import react from "react"
import "../styles/AudioPage.css";
function AudioPage() {
    return (
        <>
            <h1>Youtube Extractor</h1>
            <div>
                <input type="text" placeholder="Please parse your youtube URL here" name="youtubeUrl" className="url-input"></input>
            </div>
        </>
    )
}

export default AudioPage;