import react from "react";
import '../styles/index.css';
import "../styles/HomePage.css";
import Button from 'react-bootstrap/Button';
import { NavLink } from "react-router-dom";

function HomePage() {
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
                <div>
                    <NavLink to="/audio">
                        <Button variant="outline-danger">Download Audio</Button>
                    </NavLink>
                    <NavLink to="/video">
                        <Button variant="outline-danger">Download Video</Button>
                    </NavLink>
                </div>
                
            </div>
        </>
    );
}

export default HomePage;
