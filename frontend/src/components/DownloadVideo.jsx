import react from "react";
import "../styles/DownloadVideo.css";
import {NavLink} from "react-router-dom";
import Button from "react-bootstrap/esm/Button";
const DownloadVideo = ({ videoDetails, onDownloadResolution }) => {
    return (
        <div className="download-video">
            <h1>Download Video</h1>
            <h2>{videoDetails.title}</h2>
            <p>Duration: {videoDetails.duration}</p>
            <p>Views: {videoDetails.views}</p>
            <p>Uploader: {videoDetails.uploader}</p>
        </div>
    )
}

export default DownloadVideo;