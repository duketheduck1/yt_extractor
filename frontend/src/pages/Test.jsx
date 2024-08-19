// import React, {useState} from "react";

// function Test() {
//     const [count, setCount] = useState(0);

//     return(
//         <div>
//             <p>You clicked {count} times</p>
//             <button onClick={() => setCount(count+1)}>Click</button>
//         </div>
//     );
// };

// export default Test;

import React, { useState } from "react";

function Test() {
  const [url, setUrl] = useState("");
  const [videoData, setVideoData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchVideoData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/load-meta-data/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      if (response.ok) setVideoData(data);
      else console.error("Error:", response.statusText);
    } catch (error) {
      console.error("Error fetching video data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>Test YouTube Data Fetch</h1>
      <input
        type="text"
        placeholder="Enter YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={fetchVideoData}>Fetch Video Data</button>
      {isLoading ? <p>Loading...</p> : videoData && (
        <div>
          <h2>Video Metadata</h2>
          <p><strong>Title:</strong> {videoData.title}</p>
          <p><strong>Duration:</strong> {videoData.duration}</p>
          <p><strong>Views:</strong> {videoData.views}</p>
          <p><strong>Uploader:</strong> {videoData.uploader}</p>
          <p><strong>URL:</strong> {videoData.url}</p>
          {videoData.resolution && (
            <ul>
              {videoData.resolution.map((res, index) => (
                <li key={index}>{res}p</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default Test;
