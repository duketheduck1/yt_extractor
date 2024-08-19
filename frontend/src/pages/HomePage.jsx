import React, {react, useState, useEffect} from "react";
import "../styles/HomePage.css";
import Button from 'react-bootstrap/Button';
import { NavLink } from "react-router-dom";
import DownloadAudio from "../components/DownloadAudio";
import DownloadVideo from "../components/DownloadVideo";
// import axios from "axios";

const HomePage = () => {
    const [url, setUrl] = useState("");
    const [videoData, setVideoData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    

    return (
        <>
            <h1 className="header"> Youtube Extractor </h1>
            
            <div className="center">
                <input
                    type="text"
                    placeholder="Please parse your youtube URL here"
                    name="youtubeUrl"
                    className="url-input"
                ></input>

                {/* <div>
                    <NavLink to="/audio">
                        <Button variant="outline-danger">Download Audio</Button>
                    </NavLink>
                    <NavLink to="/video">
                        <Button variant="outline-danger">Download Video</Button>
                    </NavLink>
                </div> */}
                
            </div>
        </>
    );
}

export default HomePage;
