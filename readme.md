# YouTube Extractor

YouTube Extractor is a web application that allows users to download YouTube videos and audio in various formats and resolutions. It is built using **Django** for the backend and **React** for the frontend, with `yt-dlp` as the core library for video extraction.

## Features

- **Video Metadata Extraction**: Fetch video details such as title, duration, views, uploader, and available resolutions.
- **Video and Audio Downloads**: Download videos in MP4 format or audio in MP3 format.
- **Preview Videos**: Watch a preview of the video before downloading.
- **Responsive Design**: A clean and responsive user interface built with TailwindCSS.

## Tech Stack

### Backend
- **Django**: Python web framework for the backend.
- **Django REST Framework**: For building RESTful APIs.
- **yt-dlp**: A powerful library for YouTube video extraction.
- **PostgreSQL**: Database for storing application data.

### Frontend
- **React**: JavaScript library for building user interfaces.
- **Vite**: Fast development build tool.
- **TailwindCSS**: Utility-first CSS framework for styling.

## Installation

### Prerequisites
- Python 3.8+ (Backend)
- Node.js 16+ (Frontend)
- PostgreSQL (Database)
- Frontend Dependencies:
  - @tailwindcss/vite: ^4.0.17
  - axios: ^1.8.4
  - react: ^19.0.0
  - react-dom: ^19.0.0
  - tailwindcss: ^4.0.17
  - wouter: ^3.7.0

### Backend Setup

1. **Clone the repository**  
```bash
git clone https://github.com/your-username/yt_extractor.git
cd yt_extractor/backend
```

2. **Create a virtual environment and activate it**  
```bash
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Configure the database**  
Open `backend/settings.py` and update the `DATABASES` section:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Apply migrations**  
```bash
python manage.py migrate
```

6. **Start the backend server**  
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to the frontend directory**  
```bash
cd ../frontend
```

2. **Install dependencies**  
```bash
npm install
```

3. **Start the development server**  
```bash
npm run dev
```

4. **Open the application** in your browser at [http://localhost:5173](http://localhost:5173)

## Usage

![image](https://github.com/user-attachments/assets/260990da-7619-4a3e-8fd2-7b37409c182a)
1. Paste a YouTube URL into the search bar on the homepage.
![image](https://github.com/user-attachments/assets/9f59db0b-fe73-48c3-92e0-4209c33e210f)
2. View video details and available resolutions.
![image](https://github.com/user-attachments/assets/9f59db0b-fe73-48c3-92e0-4209c33e210f)
3. Preview the video or download it in your preferred format and resolution.
4. Overall websites view on Ipad.  
![image](https://github.com/user-attachments/assets/c282d1c8-5a80-45ad-a849-a32dab209705)
5. Overall websites view on Phone.  
![image](https://github.com/user-attachments/assets/9bd36fc6-9885-4112-8577-26a1d9fa17a2)




## API Endpoints

### `/api/load-meta-data/` (POST)
- **Description**: Fetch metadata for a YouTube video.
- **Request Body**:
```json
{
  "url": "https://www.youtube.com/watch?v=example"
}
```

- **Response**:
```json
{
  "url": "https://www.youtube.com/watch?v=example",
  "title": "Example Video",
  "duration": "00:05:30",
  "views": 123456,
  "uploader": "Example Uploader",
  "resolution": [144, 360, 720, 1080],
  "download_options": {
    "video_formats": ["mp4", "webm"],
    "audio_formats": ["mp3", "m4a", "wav"]
  }
}
```

### `/api/download/<filename>` (GET)
- **Description**: Download a video or audio file.

### `/api/preview-video/<filename>` (GET)
- **Description**: Preview a video before downloading.

## ToDo

- [x] Mobile responsiveness – UI works well on small screens.
- [ ] Dark Mode / Light Mode switch.
- [ ] Enable sharing functionality (if legally compliant).
- [x] Support multiple formats (e.g. MP3, 720p, 1080p).
- [x] Add input validation for YouTube URLs on the frontend.
- [x] Improve error handling on both frontend and backend (e.g. invalid URLs, download failures).
- [ ] Add basic CI/CD for automated testing and deployment.
- [ ] Refactor frontend by updating `style.css` – it is still a mess.
- [ ] Add thumbnail support for YouTube videos.
- [ ] Add a timer to delete cached preview videos or thumbnails.
- [x] Write unit tests for backend APIs and frontend components.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
This tool is intended strictly for personal use. Please comply with all applicable copyright laws and YouTube’s terms of service.




