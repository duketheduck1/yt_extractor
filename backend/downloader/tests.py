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

# load ytdlp data       
def load_specific_data(url: str):
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)

            # Extract the formats list
            video_stream = []
            formats = meta.get("formats", [])
            for i in formats:
                resolution = "audio only"
                if i["height"] != None:
                    resolution = f"{i["height"]} x {i["width"]}"
                video_stream.append(
                    {
                        "resolution": resolution,
                        "size": i["filesize"],
                        "url": url,
                    }
                )
            for i in video_stream:
                print(i)
       
    except Exception:
        print("There is no such url")

if __name__ == "__main__":
    URL = 'https://www.youtube.com/watch?v=bqNvkAfTvIc'
    load_specific_data(URL)