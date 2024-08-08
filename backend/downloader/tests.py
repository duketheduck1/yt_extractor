from django.test import TestCase

# Create your tests here.
import json
import yt_dlp

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
                        "url": i["url"], #url to download youtube video link
                    }
                )
            for i in range(len(video_stream)):
                print(i)
                print(video_stream[i])

        download_video_file_hosted(video_stream[5]["url"])    
            
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

if __name__ == "__main__":
    URL = 'https://www.youtube.com/watch?v=bqNvkAfTvIc'
    load_specific_data(URL)