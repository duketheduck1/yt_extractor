from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json
import re
import yt_dlp


def validate_youtube_url(url: str) -> bool:
    
    if isinstance(url, str) == True:
        if "shorts" not in url:
            yt_regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            youtube_match = re.match(yt_regex, url)
            return youtube_match is not None
        elif "shorts" in url:
            short_regex = "^(?:https?:\/\/)?(?:www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)([\w\-]+)"
            short_match = re.match(short_regex, url)
            return short_match is not None
    else:
        return False
