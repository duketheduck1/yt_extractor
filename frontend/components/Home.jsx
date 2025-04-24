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
                <h2 className="text-white text-xl font-bold mb-4">
                  About YouTube Extractor
                </h2>
                <p className="text-[#AAAAAA] mb-4">
                  YouTube Extractor is a personal-use tool designed to help
                  users download YouTube videos for offline viewing. It uses the
                  open-source project{" "}
                  <code className="bg-[#333333] text-green-400 px-1 rounded">
                    yt-dlp
                  </code>{" "}
                  library to support various formats and quality options, all
                  accessible through a clean and responsive interface.
                </p>
                <p className="text-[#AAAAAA] mb-4">
                  Built with React and Django (previously Node.js), this project
                  showcases modern web development practices, API integration,
                  and user-centered design.
                </p>
                <p className="text-[#AAAAAA]">
                  <strong className="text-primary">Note:</strong> This tool is
                  intended strictly for personal use. It is a personal
                  project which has no advertising or monetization purposes. Please comply
                  with all applicable copyright laws and YouTube’s terms of
                  service. If you are a copyright holder and have concerns, feel
                  free to contact me.
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
