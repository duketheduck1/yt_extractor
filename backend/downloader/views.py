from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import timedelta
from django.http import HttpResponse
from django.conf import settings
import os
import json
import re
import yt_dlp

# matching youtube url regex
def _validate_youtube_url(url: str) -> bool:
    if isinstance(url, str) == True:
        #check if url is a normal youtube url
        if "shorts" not in url:
            yt_regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            youtube_match = re.match(yt_regex, url)
            return youtube_match is not None
        #check if url is short youtube url
        elif "shorts" in url:
            short_regex = "^(?:https?:\/\/)?(?:www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)([\w\-]+)"
            short_match = re.match(short_regex, url)
            return short_match is not None
    else:
        return False

@api_view(["POST"])
def load_youtube_data(request):
    try:
        print("Loading video from youtube")
        url = request.data.get('url') #in json form
        '''
        Cheatsheet for request
        {
            "url": "https://www.youtube.com/watch?v=BaW_jenozKc"
        }
        '''
        if _validate_youtube_url(url):
            ydl_opts = {
                'quiet': True,  # Suppress the download output
            }

            with yt_dlp.YoutubeDL({}) as ydl:
                meta = ydl.extract_info(url, download=False)
                formats = meta.get('formats', [])

            # list of resolution to choose from ( res(p) = 1440, 1080, 720, 480, 360, 240, 144 )
            list_resolution = _list_yt_resolution(formats) 

            #context about url, title, duration, views, uploader and list of resolution
            context = { 
                "url": url,
                "title": meta.get("title", None),
                "duration":str(timedelta(seconds=meta.get("duration", 1))),
                "views":meta.get("view_count", 1),
                "uploader":meta.get("uploader", None),
                "resolution": list_resolution, 
            }

            return Response(context, status=200)
        else:
            return Response("Please input correct url.", status=400)
    except Exception as e:
        return Response(e.args[0], status=400)
    
def _list_yt_resolution(formats: list) -> list:
    # List available resolutions
    resolutions = set()
    res_basic = ["1440", "1080", "720", "480", "360", "240"]
    for format in formats:
        resolution = format.get('format_note')
        if resolution and resolution[0].isdigit():# and resolution in res_basic:
            resolutions.add(resolution)

    list_resolution_string = sorted(list(resolutions))
    list_int_resolution = _update_resolution_list(list_resolution_string)
    return list_int_resolution

#from "1080p" string to 1080
def _update_resolution_list(resolutions: list) -> list: 
    res = []

    for i in range(len(resolutions)):
        res.append(int(resolutions[i][:len(resolutions[i])-1]))

    res = sorted(res)
    return res

# This function will get the url and 1 resolution choice from context["resolution"]
@api_view(["POST"])
def download_video(url, resolution_choice): 
    all_resolutions = _list_yt_resolution(url)
    if resolution_choice not in all_resolutions:
        raise ValueError("This resolution does not exist for the url")
    ydl_opts = {
        "format": f"bestvideo[height<={resolution_choice}]+bestaudio/best",
        "merge_output_format": "webm",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


@api_view(['GET'])
def download_file(request, filename):
    url, res, ex_file = make_info(filename)
    try:
        # Check URL validity and file extension
        if _validate_youtube_url(url) and (ex_file in 'mp4|mp3'):
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            ex_file = filename[-3:]

            # If the file doesn't exist, try to download it
            if not os.path.exists(file_path):
                get_video(url, res, ex_file, filename)

            # Check again if the file exists after the download attempt
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type=f'application/{ex_file}')
                    response['Content-Disposition'] = f'attachment; filename="{filename}"'
                    return response
            else:
                # Return a 404 response if the file is still not found
                return Response({"error": "File not found"}, status=404)
        else:
            # Return a 400 response for an invalid URL or file extension
            return Response({"error": "Invalid URL or file extension"}, status=400)

    except Exception as e:
        # Catch any other exceptions and return a 500 Internal Server Error
        return Response({"error": str(e)}, status=500)    

def get_video(url, res, ex_file, filename, max_retries=3, delay=5):
    
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # Configure yt-dlp options for video or audio downloads
    if ex_file == 'mp3':
        ydl_opts = {
            'format': 'm4a/bestaudio/best',            
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ex_file,
            }],
            'outtmpl': file_path[0:len(file_path)-4],
            'retries': max_retries  # yt-dlp retry option
        }
    else:
        ydl_opts = {
            "format": f"bestvideo[height<={res}]+bestaudio/best",  # Best video and audio
            "merge_output_format": ex_file,  # Merge into mp4, mkv, etc.
            "outtmpl": file_path,  # Output path
            "postprocessors": [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': ex_file,  # Convert to specific format (mp4, mkv, etc.)
            }],
            'socket_timeout': 60,  # Set socket timeout to 60 seconds
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(result)
        return file_path



def make_info(filename):

    ex_file = filename[-3:]
    lenfile = len(filename)
    url ="https://www.youtube.com/watch?v="+filename[1:lenfile-8]
    
    res = int(filename[lenfile-8:lenfile-4])  
    return url,res,ex_file

