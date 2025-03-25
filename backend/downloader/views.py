from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import timedelta
from django.http import HttpResponse
from django.conf import settings
import logging
import os
import json
import re
import yt_dlp

# Set up logging
logger = logging.getLogger(__name__)

MAIN_RESOLUTIONS = [144,360,720,1080]
SUPPORTED_FORMATS = {
    'video': ['mp4', 'webm'],
    'audio': ['mp3', 'm4a', 'wav']
}

# validate if a URL is a Youtube url by using regex matching
def _validate_youtube_url(url: str) -> tuple[bool,str]:

    if not url:
        return False, "URL is required"

    if not isinstance(url,str):
        return False, "URL must be a string"

    if "shorts" not in url:
        yt_regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        is_valid_url = re.match(yt_regex, url) is not None
    else:
        short_regex = "^(?:https?:\/\/)?(?:www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)([\w\-]+)"
        is_valid_url = re.match(short_regex, url) is not None
            
    return is_valid_url, "please provide a valid Youtube URL" if not is_valid_url else ""

def get_available_resolution(formats):
    available_resolutions = set()
    for format_info in formats:
        resolution  = format_info.get('height')

        if resolution and resolution in MAIN_RESOLUTIONS:
            available_resolutions.add(resolution)
    return sorted(list(available_resolutions))

@api_view(["POST"])
def load_youtube_data(request):
    """Load metadata from a YouTube video URL.

    Cheatsheet for request on http://localhost:8000/api/load-meta-data/
    
    Request body:
    {
        "url": "https://www.youtube.com/watch?v=YeNBsW0Slrk"
    }
    
    Returns:
        Response: Video metadata or error message
    """
    try:
        logger.info("Loading youtube metadata from Youtube")
        url = request.data.get('url') #in json form

        is_valid, error_message = _validate_youtube_url(url)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl: #'quiet': True --> suppress download output      
            meta = ydl.extract_info(url, download=False)                
            formats = meta.get('formats',[])    
        
        #Get available resolutions
        available_resolution = get_available_resolution(formats)

        #Response infomation
        response_data = {
            "url": url,
            "title": meta.get("title", "Unknown"),
            "duration":str(timedelta(seconds=meta.get("duration", 0))),
            "views":meta.get("view_count", 0),
            "uploader":meta.get("uploader", "Unknown"),
            "resolution": available_resolution, 
            "download_options": {
                "video_formats": SUPPORTED_FORMATS['video'],
                "audio_formats": SUPPORTED_FORMATS['audio']
            }
        }    
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        logger.info(f"Error loading Youtube data: {str(e)}")
        return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def download_media(request):
    try:
        url = request.data.get('url')
        download_type = request.data.get('type','video')
        file_format = request.data.get('format','mp4')
        resolution = request.data.get('resolution')

        # Validate input URL
        is_valid, error_message = _validate_youtube_url(url)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        #validate download type in video', 'audio', or 'video_no_audio' 
        if download_type not in ['video', 'audio', 'video_no_audio']:
            return Response(
                {"error": "Download type must be 'video', 'audio', or 'video_no_audio' "}, status=status.HTTP_400_BAD_REQUEST
            )
        
        #supported format
        supported_formats = (
            SUPPORTED_FORMATS['video'] 
            if download_type in ['video', 'video_no_audio'] 
            else SUPPORTED_FORMATS['audio']
        )
        if file_format not in supported_formats:
            return Response(
                {"error": f"Supported formats are: {supported_formats}"},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        
        #Download type
        if download_type == "video": #video with audio
            try:
                resolution = int(resolution)
            except (ValueError, TypeError):
                return Response(
                    {"error":"Resolution must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if resolution not in MAIN_RESOLUTIONS:
                return Response(
                    {"error": f"Supported resolutions are: {MAIN_RESOLUTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ydl_opts = {
                'format': f'bestvideo[height<={resolution}]+bestaudio/best',            
                'merge_output_format': file_format,
            }

        elif download_type == "vodep_no_audio": #video no audio
            try:
                resolution = int(resolution)
            except (ValueError, TypeError):
                return Response(
                    {"error":"Resolution must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if resolution not in MAIN_RESOLUTIONS:
                return Response(
                    {"error": f"Supported resolutions are: {MAIN_RESOLUTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            ydl_opts = {
                'format': f'bestvideo[height<={resolution}]',            
                'merge_output_format': file_format,
            }

        else:#audio only
            
            dl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': file_format
                }]
            }


        #TODO: need to add download path and directory
        

    except Exception as e:
        logger.error(f"Error in download process: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    


# # This function will get the url and 1 resolution choice from context["resolution"]
# @api_view(["POST"])
# def download_video(url, resolution_choice): 
#     all_resolutions = _list_yt_resolution(url)
#     if resolution_choice not in all_resolutions:
#         raise ValueError("This resolution does not exist for the url")
#     ydl_opts = {
#         "format": f"bestvideo[height<={resolution_choice}]+bestaudio/best",
#         "merge_output_format": "webm",
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download(url)


# @api_view(['GET'])
# def download_file(request, filename):
#     url, res, ex_file = make_info(filename)
#     try:
#         # Check URL validity and file extension
#         if _validate_youtube_url(url) and (ex_file in 'mp4|mp3'):
#             file_path = os.path.join(settings.MEDIA_ROOT, filename)
#             ex_file = filename[-3:]

#             # If the file doesn't exist, try to download it
#             if not os.path.exists(file_path):
#                 get_video(url, res, ex_file, filename)

#             # Check again if the file exists after the download attempt
#             if os.path.exists(file_path):
#                 with open(file_path, 'rb') as f:
#                     response = HttpResponse(f.read(), content_type=f'application/{ex_file}')
#                     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#                     return response
#             else:
#                 # Return a 404 response if the file is still not found
#                 return Response({"error": "File not found"}, status=404)
#         else:
#             # Return a 400 response for an invalid URL or file extension
#             return Response({"error": "Invalid URL or file extension"}, status=400)

#     except Exception as e:
#         # Catch any other exceptions and return a 500 Internal Server Error
#         return Response({"error": str(e)}, status=500)    


# def get_video(url, res, ex_file, filename, max_retries=3, delay=5):
    
#     file_path = os.path.join(settings.MEDIA_ROOT, filename)

#     # Configure yt-dlp options for video or audio downloads
#     if ex_file == 'mp3':
#         ydl_opts = {
#             'format': 'm4a/bestaudio/best',            
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': ex_file,
#             }],
#             'outtmpl': file_path[0:len(file_path)-4],
#             'retries': max_retries  # yt-dlp retry option
#         }
#     else:
#         ydl_opts = {
#             "format": f"bestvideo[height<={res}]+bestaudio/best",  # Best video and audio
#             "merge_output_format": ex_file,  # Merge into mp4, mkv, etc.
#             "outtmpl": file_path,  # Output path
#             "postprocessors": [{
#                 'key': 'FFmpegVideoConvertor',
#                 'preferedformat': ex_file,  # Convert to specific format (mp4, mkv, etc.)
#             }],
#             'socket_timeout': 60,  # Set socket timeout to 60 seconds
#         }
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         result = ydl.extract_info(url, download=True)
#         file_path = ydl.prepare_filename(result)
#         return file_path



# def make_info(filename):

#     ex_file = filename[-3:]
#     lenfile = len(filename)
#     url ="https://www.youtube.com/watch?v="+filename[1:lenfile-8]
    
#     res = int(filename[lenfile-8:lenfile-4])  
#     return url,res,ex_file
