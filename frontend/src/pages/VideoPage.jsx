import react from "react";
import "../styles/VideoPage.css";
import {NavLink} from "react-router-dom";
import Button from "react-bootstrap/esm/Button";
function VideoPage() {
    return (
        <>
            <h1>Youtube Extractor</h1>
            <div>
                <NavLink to="/">
                    <Button variant="outline-danger" >Home</Button>
                </NavLink>
            </div>
        </>
    )
}

export default VideoPage;