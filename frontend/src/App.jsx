import { useState, react } from 'react';
import {Route, Routes, BrowserRouter, Navigate} from "react-router-dom";
import HomePage from "./pages/HomePage";
import AudioPage from "./pages/AudioPage";
import VideoPage from "./pages/VideoPage";

function App() {

  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/audio" element={<AudioPage/>}/>
          <Route path="/video" element={<VideoPage/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
