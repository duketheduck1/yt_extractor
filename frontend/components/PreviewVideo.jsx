import React, { useState } from "react";
import axios from 'axios';

const VideoPreview = ({ url, res }) => {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const closeVideo = () => {
    setPreviewUrl(null);
    setIsOpen(false);
  }
  const playVideo = async() => {
    try {
      const response = await axios.get(url);
      if (response.status === 200) {
        setPreviewUrl(response.data);
        setIsOpen(true);
      } else {
        console.error('Error fetching video data:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching video data:', error);
      setError(error.response?.data?.error || 'Failed to fetch video info');
    }
  }

  return (
    <div>
      <button
        onClick={playVideo}
        style={{ color: 'blue', textDecoration: 'underline', background: 'none', border: 'none', cursor: 'pointer' }}
      >
        view{res}p
      </button>
      
      {isOpen && previewUrl && (
        <div style={{ marginTop: '10px' }}>
          <button onClick={closeVideo}>Close</button>
          <video width="480" controls>
            <source src={previewUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default VideoPreview;