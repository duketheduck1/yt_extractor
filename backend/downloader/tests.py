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
def load_video_data(url: str):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)

            # Extract the formats list
            video_stream = []
            formats = meta.get('formats', [])
            for i in formats:
                resolution = "audio only"
                if i.get('height') == None:
                    continue
                else:
                    resolution = f"{i['height']} x {i['width']}"
                video_stream.append( #showing all size of stream
                    {
                        "resolution": resolution,
                        "size": i.get("filesize", None), # cant use i["filesize"] since there are some stream with unknown filesize 
                        # "url": i["url"],
                    }
                )
            for i in range(len(video_stream)):
                print(i)
                print(video_stream[i])

        # download_video_file_hosted(video_stream[5]["url"])    
            
    except:
        print("Something is wrong")

def download_video_file_hosted(chosen_url):
    ydl_opts = {
        'format': 'besvideo/best',
        'outtmpl':'downloaded_video.mp3',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([chosen_url])
                print("Download complete!")
    except Exception as e:
        print(f"Failed to download video: {e}")

def validate_youtube_url(url: str) -> bool:
    if isinstance(url, str) == True:
        if "shorts" not in url:
            yt_regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
            youtube_match = re.match(yt_regex, url)
            print(youtube_match == None)
        elif "shorts" in url:
            short_regex = "^(?:https?:\/\/)?(?:www\.)?(youtube\.com\/(watch\?v=|shorts\/)|youtu\.be\/)([\w\-]+)"
            short_match = re.match(short_regex, url)
            print(short_match == None)
    else:
        return False

if __name__ == "__main__":
    URL = 'https://www.youtube.com/shorts/Tyx4YCkbd-o'
    load_specific_data(URL) 
    # validate_youtube_url(URL)
    # help(yt_dlp.postprocessor.PostProcessor)

    