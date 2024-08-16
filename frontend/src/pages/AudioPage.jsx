import react from "react";
import { NavLink } from "react-router-dom";
import "../styles/AudioPage.css";
import Button from "react-bootstrap/esm/Button";
function AudioPage() {
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

export default AudioPage;