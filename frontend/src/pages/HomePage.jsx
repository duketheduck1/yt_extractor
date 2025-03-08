import React, { react, useState, useEffect } from "react";
import "../styles/HomePage.css";
import Button from "react-bootstrap/Button";
import { NavLink } from "react-router-dom";
import axios from "axios";
import Navbar from "./Navbar";
import Footer from "./Footer";

const HomePage = () => {
  const [url, setUrl] = useState("");
  const [videoData, setVideoData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [count, setCount] = useState(0);

  const fetchVideoData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/load-meta-data/",
        { url }
      ); // Corrected destructuring
      if (response.status === 200) {
        setVideoData(response.data);
      } else {
        console.error("Error fetching video data:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching video data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="main">
      <Navbar/>
      <h1>YouTube Fetch Data</h1>

      <div className="container-input">
        <div className="conteiner-row">
          <input
            type="text"
            placeholder="Please enter your YouTube URL here"
            value={url}
            name="youtubeUrl"
            className="url-input"
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div className="button-container">
          <Button variant="outline-danger" onClick={fetchVideoData}>
            Download
          </Button>
        </div>
      </div>

      {isLoading && (
        <div class="d-flex justify-content-center p-30">
          <div class="spinner-border" role="status">
            <span class="sr-only">LOL</span>
          </div>
        </div>
      )}
      <div className="container-detail">
        {videoData && ( // videoData to check if there is data initialized and start rendering component
          <div  className="left-div">
            <h4>Video Details</h4>
            <div> <strong>Title:</strong> {videoData.title} </div>
            <div> <strong>Duration:</strong> {videoData.duration} </div>
            <div> <strong>Views:</strong> {videoData.views} </div>
            <div> <strong>Uploader:</strong> {videoData.uploader} </div>
            <div> <strong>URL:</strong> {videoData.url} </div>
          </div>
        )}
        <div className="list-center">
          {videoData && videoData.resolution && (
            
            <div>
                <div>
                    <a href={"http://localhost:8000/api/download/f"+url.split('v=')[1]+"0125.mp3/"}>Audio mp3</a>
                    
                </div>
              {videoData.resolution.map((res, index) => (
                
                <div key={index}>
                  <a href={"http://localhost:8000/api/download/f"+url.split('v=')[1]+(res.toString().length==3?"0":"") +res+".mp4/"}>{res}p</a>
                    
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <Footer/>
    </div>
  );
};

export default HomePage;
