from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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
            pass
        else:
            return Response("Please input correct url.", status=400)
    except Exception as e:
        return Response(e.args[0], status=400)
    
def _get_youtube_stream(url: str):
    pass




