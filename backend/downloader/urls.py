from django.urls import path

from downloader.views import *

urlpatterns = [
    path("load-meta-data/",load_youtube_data, name="load_youtube_data"),
    path("download/<str:filename>/",download_media, name="download_file"),
    path("preview-video/<str:filename>/",preview_video, name="preview_video"),
]
