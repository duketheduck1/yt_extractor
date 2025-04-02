import { useState, react } from 'react';
import {Route, Routes, BrowserRouter, Navigate} from "react-router-dom";
import HomePage from "./pages/HomePage";
import Test from "./pages/Test";


function App() {

  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/test" element={<Test/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
