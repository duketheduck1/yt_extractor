import react from "react";
import { NavLink } from "react-router-dom";
import "../styles/DownloadAudio.css";
import Button from "react-bootstrap/esm/Button";
function DownloadAudio() {
    return (
        <>
            <div>
                
                <NavLink to="/">

                    <Button variant="outline-danger" >Home</Button>
                </NavLink>
            </div>
        </>
    )
}

export default DownloadAudio;