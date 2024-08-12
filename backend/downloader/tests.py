from django.test import TestCase
import json
import yt_dlp
import re 

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
def load_specific_data(url: str):
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
                        # "url": i["url"], 
                        "asr": i.get("asr", None)
                    }
                )
            for i in range(len(video_stream)):
                print(i)
                print(video_stream[i])

        # download_video_file_hosted(video_stream[15]["url"])    
            
    except:
        print("Something is wrong")

def download_video_file_hosted(chosen_url):
    ydl_opts = {
        'format': 'besvideo/best',
        'outtmpl':'downloaded_video.mp4',
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
def list_resolutions(url) -> list:
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
        l = sorted(list(resolutions))
        print(f"Available resolutions for {url}:")
        resolutions = l
        for resolution in resolutions:
            print(f"- {resolution}")

        
        return l
    


if __name__ == "__main__":
    URL = "https://www.youtube.com/watch?v=kKAue9DiHc0&t=2s"
    # load_specific_data(URL) 
    # download_audio(URL)
    list_resolutions(URL)
    

    
    
    

    