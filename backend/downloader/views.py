from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import timedelta
# from django.http import HttpResponse
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
        url = request.data.get('url')
        
        if _validate_youtube_url(url):
            with yt_dlp.YoutubeDL({}) as ydl:
                meta = ydl.extract_info(url, download=False)

            context = { #context about title, duration, views and uploader
                "title": meta.get("title", None),
                "duration":str(timedelta(seconds=meta.get("duration", 1))),
                "views":meta.get("view_count", 1),
                "uploader":meta.get("uploader", None),
            }

            
        else:
            return Response("Please input correct url.", status=400)
    except Exception as e:
        return Response(e.args[0], status=400)
    
def _list_yt_resolution(url: str):
    ydl_opts = {
        'quiet': True,  # Suppress the download output
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract the video information
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

        # List available resolutions
        resolutions = set()
        for format in formats:
            resolution = format.get('format_note')
            if resolution and resolution[0].isdigit():
                resolutions.add(resolution)
        list_resolution_string = sorted(list(resolutions))
        print(f"Available resolutions for {url}:")
        list_int_resolution = _get_resolution(list_resolution_string)
        return list_int_resolution

def _get_resolution(resolutions: list): #from "1080p" string to 1080
    res = []
    for i in range(len(resolutions)):
        res.append(int(resolutions[i][:len(resolutions[i])-1]))
    res = sorted(res)
    return res

def _download_resolution(url, resolution_choice):
    all_resolutions = _list_yt_resolution(url)
    if resolution_choice not in all_resolutions:
        raise ValueError("This resolution does not exist for the url")
    ydl_opts = {
        "format": f"bestvideo[height<={resolution_choice}]+bestaudio/best",
        "merge_output_format": "webm",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)




