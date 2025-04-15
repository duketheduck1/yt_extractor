import React, { useState } from "react";

function VideoPreviewComponent({ url, index, res }) {
  const [previewUrl, setPreviewUrl] = useState(null);

  const videoUrl = `http://localhost:8000/api/download/f${url.split('v=')[1]}${res.toString().length === 3 ? "0" : ""}${res}.mp4/`;

  return (
    <div key={index}>
      <button
        onClick={() => setPreviewUrl(videoUrl)}
        style={{ color: 'blue', textDecoration: 'underline', background: 'none', border: 'none', cursor: 'pointer' }}
      >
        {res}p
      </button>

      {previewUrl === videoUrl && (
        <div style={{ marginTop: '10px' }}>
          <video width="480" controls>
            <source src={previewUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}
