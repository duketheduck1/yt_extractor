from django.test import TestCase
import json
import yt_dlp
import re 
from datetime import timedelta

# Create your tests here.
# Test ytdlp output meta data to file

def output_to_file(url: str):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)

        # Extract the formats list
        formats = meta.get('formats', [])

        #save all formats to test.txt file
        if formats:
            with open("test.txt", "w") as file:
                for line in formats:
                    file.write(json.dumps(line, indent=2)+"\n\n")
        else:
            print("No formats available")

# show youtube audio and stream    
def load_data(url: str):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)

            # Extract the formats list
            video_stream = []
            formats = meta.get('formats', [])
            for i in formats:
                resolution = "audio only"
                if i.get('height') != None:
                    resolution = f"{i['height']} x {i['width']}"
                video_stream.append( #showing all size of stream
                    {
                        "resolution": resolution,
                        "size": i.get("filesize", None), # cant use i["filesize"] since there are some stream with unknown filesize 
                        "url": i["url"], 
                        "asr": i.get("asr", None)
                    }
                )
            for i in range(len(video_stream)):
                print(i)
                print(video_stream[i])

        download_video_file_hosted(video_stream[15]["url"])    
            
    except:
        print("Something is wrong")

def download_video_file_hosted(chosen_url):
    ydl_opts = {
        'format': 'besvideo/best',
        'outtmpl':'downloaded_video.webm',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([chosen_url])
                print("Download complete!")
    except Exception as e:
        print(f"Failed to download video: {e}")

#download audio
def download_audio(url):
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)


#list resolution for video
def list_video_resolutions(url) -> list:
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
        list_string_resolution = sorted(list(resolutions))
        print(f"Available resolutions for {url}:")
        # resolutions = list_string_resolution
        # for resolution in resolutions:
        #     print(f"{resolution}")
        list_int_resolution = get_resolution(list_string_resolution)
        return list_int_resolution
    
def get_resolution(resolutions: list):
    res = []
    for i in range(len(resolutions)):
        res.append(int(resolutions[i][:len(resolutions[i])-1]))
    res = sorted(res)
    return res

def download_video(url, resolution_choice: int):
    all_resolutions = list_video_resolutions(url)
    if resolution_choice not in all_resolutions:
        raise ValueError("This resolution does not exist for the url")
    ydl_opts = {
        "format": f"bestvideo[height<={resolution_choice}]+bestaudio/best",
        "merge_output_format": "webm",
        
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

def get_info(url, options):
    with yt_dlp.YoutubeDL(options) as ydl:
        meta = ydl.extract_info(url, download=False)
    context = {
        "title": meta.get("title", None),
        "duration":str(timedelta(seconds=meta.get("duration", 1))),
        "views":meta.get("view_count", 1),
        "uploader":meta.get("uploader", None),
    }
    return context


MAIN_RESOLUTIONS = [144,360,720,1080]

def get_video_resolutions(video_url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            resolutions = []
            for fmt in formats:
                if fmt.get('height') in MAIN_RESOLUTIONS:
                    resolutions.append(f"{fmt['height']}")

            return resolutions if resolutions else ["No matching resolutions found."]

    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    
    URL = "https://www.youtube.com/watch?v=YeNBsW0Slrk"
    resolutions = get_video_resolutions(URL)
    print("Available Resolutions:")
    for res in resolutions:
        print(f"- {res}")
    # save_path = r"C:\Users\ducod\Downloads"
    # load_data(URL) 
    # download_audio(URL)
    # print(list_video_resolutions(URL))
    # help(yt_dlp.postprocessor)
    # download_video(URL, 360, save_path)
    # load_video_data(URL)
    
    
    
    
    

    