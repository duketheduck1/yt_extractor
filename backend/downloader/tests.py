import unittest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from .views import _validate_youtube_url

# filepath: c:\Users\ducod\OneDrive\Desktop\python\yt_extractor\backend\downloader\test_tests.py

class TestDownloaderViews(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_validate_youtube_url(self):
        # Valid YouTube URL
        valid_url = "https://www.youtube.com/watch?v=YeNBsW0Slrk"
        is_valid, error_message = _validate_youtube_url(valid_url)
        self.assertTrue(is_valid)
        self.assertEqual(error_message, "")

        # Valid YouTube Shorts URL
        valid_shorts_url = "https://www.youtube.com/shorts/YeNBsW0Slrk"
        is_valid, error_message = _validate_youtube_url(valid_shorts_url)
        self.assertTrue(is_valid)
        self.assertEqual(error_message, "")

        # Invalid URL
        invalid_url = "https://www.example.com"
        is_valid, error_message = _validate_youtube_url(invalid_url)
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "please provide a valid Youtube URL")

        # Empty URL
        empty_url = ""
        is_valid, error_message = _validate_youtube_url(empty_url)
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "URL is required")

        # Non-string URL
        non_string_url = 12345
        is_valid, error_message = _validate_youtube_url(non_string_url)
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "URL must be a string")

    @patch("yt_dlp.YoutubeDL")
    def test_load_youtube_data_valid_url(self, mock_ytdlp):
        # Mock yt_dlp response
        mock_ytdlp.return_value.__enter__.return_value.extract_info.return_value = {
            "title": "Test Video",
            "duration": 120,
            "view_count": 1000,
            "uploader": "Test Uploader",
            "formats": [{"height": 720}, {"height": 1080}],
        }

        # Valid request
        response = self.client.post(
            "/api/load-meta-data/",
            {"url": "https://www.youtube.com/watch?v=YeNBsW0Slrk"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertEqual(response.data["title"], "Test Video")
        self.assertIn("resolution", response.data)
        self.assertEqual(response.data["resolution"], [720, 1080])

    def test_load_youtube_data_invalid_url(self):
        # Invalid request
        response = self.client.post(
            "/api/load-meta-data/",
            {"url": "https://www.example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "please provide a valid Youtube URL")
    
    

    