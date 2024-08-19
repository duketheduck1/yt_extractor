import React, {react, useState, useEffect} from "react";
import "../styles/HomePage.css";
import Button from 'react-bootstrap/Button';
import { NavLink } from "react-router-dom";
import DownloadAudio from "../components/DownloadAudio";
import DownloadVideo from "../components/DownloadVideo";
// import axios from "axios";

const HomePage = () => {
    const [url, setUrl] = useState("");
    const [videoData, setVideoData] = useState(null); //update video metadata to videoData
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e) => {
        setUrl(e.target.value)
    }

    const fetchVideoData = async(type) => {
        setIsLoading(True);
        try{
            const response = await fetch("http://localhost:8000/load-meta-data/", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({url}),
            });

            if (response.ok) {
                const data = await response.json();
                setVideoData = data;
            }else{
                console.error("Error fetching data:", response.statusText);
            } 

        }catch(error){
            console.error("Error fetching data:", error);
        }
    
    }

    return (
        <>
            <h1 className="header"> Youtube Extractor </h1>
            
            <div className="center">
                <input
                    type="text"
                    placeholder="Please parse your youtube URL here"
                    name="youtubeUrl"
                    className="url-input"
                    value={url}
                    onChange={handleInputChange}
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
