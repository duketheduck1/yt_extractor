import React, { useState } from "react";
import axios from "axios";
import "../styles/HomePage.css";
import Button from "react-bootstrap/Button"; // Corrected import path

function Test() {
    const [url, setUrl] = useState("");
    const [videoData, setVideoData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const fetchVideoData = async () => {
        setIsLoading(true);
        try {
            const response = await axios.post("http://localhost:8000/api/load-meta-data/", { url }); // Corrected destructuring
            if (response.status === 200) {
                setVideoData(response.data);
            } else {
                console.error("Error fetching video data:", response.statusText);
            }
        } catch(error) {
            console.error("Error fetching video data:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h1>YouTube Fetch Data</h1>
            <div>
                <input
                    type="text"
                    placeholder="Please enter your YouTube URL here"
                    value={url}
                    name="youtubeUrl"
                    className="url-input"
                    onChange={(e) => setUrl(e.target.value)}
                />
            </div>
            <div>
                <Button variant="outline-danger" onClick={fetchVideoData}>
                    Download Video
                </Button>
            </div>

            {isLoading && (
                <div className="loading-container">
                    <div className="loading-bar"></div>
                </div>
            )}

            {videoData && ( // videoData to check if there is data initialized and start rendering component
                <div>
                    <h2>Video Details</h2>
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

