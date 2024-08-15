import react from "react";
import "../styles/HomePage.css";
import {NavLink} from "react-router-dom"

function HomePage() {
    return (
        <>
            <h1>Youtube Extractor</h1>
            <div>
                <input type="text" placeholder="Please parse your youtube URL here" name="youtubeUrl" className="url-input"></input>
                <NavLink to="/audio">
                    <button>Download Audio</button>
                </NavLink >
                <NavLink to="/video">
                    <button>Download Video</button>
                </NavLink >
            </div>
        </>
    )
}

export default HomePage;