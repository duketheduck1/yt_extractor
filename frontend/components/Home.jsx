import React from "react";
import "../styles/index.css";
import Nav from "./Nav";
import Searchbar from "./Searchbar";
import Footer from "./Footer";
const Home = () => {
  return (
    <div className="flex flex-col min-h-screen bg-[#121212]">
      <Nav />
      <main className="flex-grow">
        <Searchbar />
        {/* About Section */}
        <section id="about" className="py-16 bg-[#1A1A1A]">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              <h2 className="text-3xl font-bold text-white text-center mb-6">
                About This Project
              </h2>
              <div className="bg-[#242424] p-6 rounded-lg shadow-lg">
                <p className="text-[#AAAAAA] mb-4">
                  Youtube Extractor is a project built to allow downloading
                  YouTube videos for personal use. The application provides a
                  simple and intuitive interface to search, preview, and
                  download videos in different formats and qualities.
                </p>
                <p className="text-[#AAAAAA] mb-4">
                  Built with React and Node.js, this project serves as a
                  demonstration of modern web development techniques,
                  asynchronous API calls, and user interface design.
                </p>
                <p className="text-[#AAAAAA]">
                  <strong className="text-primary">Note:</strong> This service
                  is intended for personal use only. Please respect copyright
                  laws and YouTube's terms of service when using this
                  application.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Home;
