# validate if a URL is a Youtube url by using regex matching
# def _validate_youtube_url(url: str) -> bool:

#     if not isinstance(url,str):
#         return False

#     if "shorts" not in url:
#         yt_regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
#         return re.match(yt_regex, url) is not None
            
#     short_regex = "^(?:https?:\/\/)?(?:www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)([\w\-]+)"
#     return re.match(short_regex, url) is not None

# # def get_available_resolution(formats):
# #     available_resolutions = set()
# #     for format_info in formats:
# #         resolution  = format_info.get('format_note', '')

# #         print(f"Format note: {resolution}")

# #         if resolution and any(char.isdigit() for char in resolution):
# #             try:
# #                 #Extract numeric resolution
# #                 res = int(''.join(filter(str.isdigit, resolution)))

# #                 #filter for main resolutions:
# #                 if res in MAIN_RESOLUTIONS:
# #                     available_resolutions.add(res)
# #             except ValueError:
# #                 continue
# #     return sorted(list(available_resolutions))

# @api_view(["POST"])
# def load_youtube_data(request):
#     """Load metadata from a YouTube video URL.

#     Cheatsheet for request on http://localhost:8000/api/load-meta-data/
    
#     Request body:
#     {
#         "url": "https://www.youtube.com/watch?v=YeNBsW0Slrk"
#     }
    
#     Returns:
#         Response: Video metadata or error message
#     """
#     try:
#         logger.info("Loading youtube metadata from Youtube")
#         url = request.data.get('url') #in json form

#         if not url: #no url input
#             return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST )
        
#         if not _validate_youtube_url(url): # incorrect url input
#             return Response({"error": "Please provide a valid YouTube URL"}, status=status.HTTP_400_BAD_REQUEST )
            
#         with yt_dlp.YoutubeDL({'quiet': True}) as ydl: #'quiet': True --> suppress download output      
#             meta = ydl.extract_info(url, download=False)                
#             formats = meta.get('formats',[])    
        
#         #Get available resolutions
#         available_resolution = get_available_resolution(formats)

#         #Response infomation
#         response_data = {
#             "url": url,
#             "title": meta.get("title", "Unknown"),
#             "duration":str(timedelta(seconds=meta.get("duration", 0))),
#             "views":meta.get("view_count", 0),
#             "uploader":meta.get("uploader", "Unknown"),
#             "resolution": available_resolution, 
#             "download_options": {
#                 "video_formats": SUPPORTED_FORMATS['video'],
#                 "audio_formats": SUPPORTED_FORMATS['audio']
#             }
#         }    
#         return Response(response_data, status=status.HTTP_200_OK)
    
#     except Exception as e:
#         logger.info(f"Error loading Youtube data: {str(e)}")
#         return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


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