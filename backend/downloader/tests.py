from django.test import TestCase

# Create your tests here.
import json
import yt_dlp

URL = 'https://www.youtube.com/watch?v=bqNvkAfTvIc'

ydl_opts = {}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)

    # Extract the formats list
    formats = info.get('formats', [])

    if formats:
        with open("test.txt", "w") as file:
            for line in formats:
                file.write(json.dumps(line, indent=2)+"\n\n")
    else:
        print("No formats available")