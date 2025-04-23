import { useState } from "react";
import axios from "axios";

const Searchbar = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [videoData, setVideoData] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [activePreview, setActivePreview] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setVideoData(null);
    setPreviewUrl(null);
    setActivePreview(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/load-meta-data/",
        { url }
      );

      if (response.status === 200) {
        setVideoData(response.data);
      } else {
        setError("Error fetching video data: " + response.statusText);
      }
    } catch (err) {
      console.error("Error fetching video data:", err);
      setError(err.response?.data?.error || "Failed to fetch video info");
    } finally {
      setLoading(false);
    }
  };

  const handlePreviewVideo = async (resolution, index) => {
    setActivePreview(index);

    try {
      // Form the video ID from the URL
      const videoId = url.includes("v=")
        ? url.split("v=")[1].split("&")[0]
        : url.split("/").pop();

      if (!videoId) {
        setError("Could not extract video ID");
        return;
      }

      const resString =
        resolution.toString().length === 3 ? `0${resolution}` : resolution;
      const previewUrl = `http://localhost:8000/api/preview-video/f${videoId}${resString}.mp4/`;
      const response = await axios.get(previewUrl);

      setPreviewUrl(response.data);
    } catch (err) {
      console.error("Error previewing video:", err);
      setError("Failed to load video preview");
    }
  };

  const getDownloadUrl = (format, resolution) => {
    // Form the video ID from the URL
    const videoId = url.includes("v=")
      ? url.split("v=")[1].split("&")[0]
      : url.split("/").pop();

    if (!videoId) return "#";

    if (format === "mp3") {
      return `http://localhost:8000/api/download/f${videoId}0125.mp3/`;
    } else {
      const resString =
        resolution.toString().length === 3 ? `0${resolution}` : resolution;
      return `http://localhost:8000/api/download/f${videoId}${resString}.mp4/`;
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-8">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="bg-[#FF0000] text-white px-3 py-1 rounded-lg">
            YouTube
          </span>{" "}
          <span className="text-primary">Downloader</span>
        </h1>
        <p className="text-[#AAAAAA] mb-6 max-w-2xl mx-auto">
          Free online tool to download YouTube videos in various formats. Just
          paste the URL below to get started.
        </p>
      </div>

      {/* Search Box */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-3xl mx-auto mb-10 transition-all"
      >
        <div className="flex flex-col md:flex-row shadow-lg">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste YouTube URL here..."
            className="search-input focus:ring-2 focus:ring-primary"
          />
          <button
            type="submit"
            disabled={loading}
            className={`py-2 px-3 ${
              loading ? "bg-indigo-700" : "bg-indigo-600 hover:bg-indigo-700"
            } text-white rounded-md text-center transition duration-150 flex items-center justify-center`}
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                <span>Loading...</span>
              </>
            ) : (
              <>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 mr-2"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                <span>Search</span>
              </>
            )}
          </button>
        </div>
        {error && (
          <div className="mt-2 p-3 bg-red-900 bg-opacity-30 text-red-300 rounded-md">
            <p>{error}</p>
          </div>
        )}
      </form>

      {/* Loading Indicator */}
      {loading && !error && (
        <div className="flex justify-center items-center py-8">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}

      {/* Video Results Section */}
      {videoData && (
        <div className="mb-16">
          {/* Video Preview Section */}
          <div className="mb-10">
            <div className="bg-[#1E1E1E] rounded-lg shadow-lg overflow-hidden">
              <div className="aspect-video w-full bg-black relative">
                {previewUrl ? (
                  <video controls className="w-full h-full">
                    <source src={previewUrl} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <div
                    className="w-full h-full flex flex-col items-center justify-center group cursor-pointer relative"
                    style={{
                      backgroundImage: videoData.thumbnail
                        ? `url(${videoData.thumbnail})`
                        : "none",
                      backgroundSize: "cover",
                      backgroundPosition: "center",
                    }}
                    onClick={() => {
                      // Auto-preview with highest available resolution
                      if (videoData.resolution.length > 0) {
                        const highestRes = Math.max(...videoData.resolution);
                        const index = videoData.resolution.indexOf(highestRes);
                        handlePreviewVideo(highestRes, index);
                      }
                    }}
                  >
                    {/* Dark overlay */}
                    <div className="absolute inset-0 bg-black bg-opacity-50 group-hover:bg-opacity-40 transition-all duration-300"></div>

                    {/* Play button and text */}
                    <div className="relative z-10 flex flex-col items-center">
                      <div className="w-16 h-16 rounded-full bg-red-600 bg-opacity-90 flex items-center justify-center mb-2 group-hover:bg-opacity-100 group-hover:scale-110 transition-all duration-300">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-8 w-8 text-white"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                          />
                        </svg>
                      </div>
                      <p className="text-white text-shadow text-center font-medium">
                        Click to play preview or select resolution below
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Video Details and Download Options */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Video Details */}
            <div className="md:col-span-1">
              <div className="bg-[#1E1E1E] rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold mb-4 text-white border-b border-gray-700 pb-2">
                  Video Details
                </h3>

                <div className="space-y-3 mt-4">
                  <div>
                    <h4 className="font-bold text-white">Title:</h4>
                    <p className="text-[#AAAAAA]">{videoData.title}</p>
                  </div>

                  <div>
                    <h4 className="font-bold text-white">Duration:</h4>
                    <p className="text-[#AAAAAA]">{videoData.duration}</p>
                  </div>

                  <div>
                    <h4 className="font-bold text-white">Views:</h4>
                    <p className="text-[#AAAAAA]">
                      {videoData.views.toLocaleString()}
                    </p>
                  </div>

                  <div>
                    <h4 className="font-bold text-white">Uploader:</h4>
                    <p className="text-[#AAAAAA]">{videoData.uploader}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Download Options */}
            <div className="md:col-span-2">
              <div className="bg-[#1E1E1E] rounded-lg shadow-lg p-6">
                <h3 className="text-xl font-bold mb-4 text-white border-b border-gray-700 pb-2">
                  Download Options
                </h3>

                <div className="space-y-6">
                  <div>
                    <h4 className="font-medium text-white mb-3">
                      Audio Format
                    </h4>
                    <a
                      href={getDownloadUrl("mp3")}
                      className="block w-full py-3 px-4 bg-gray-800 hover:bg-gray-700 text-white rounded-md text-center transition duration-150 flex items-center justify-between"
                    >
                      <span className="flex items-center">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="h-5 w-5 mr-2"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
                          />
                        </svg>
                        MP3 Audio
                      </span>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                        />
                      </svg>
                    </a>
                  </div>

                  <div>
                    <h4 className="font-medium text-white mb-3">
                      Video Formats
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {videoData.resolution.map((res, index) => (
                        <div
                          key={index}
                          className="bg-[#2A2A2A] rounded-lg p-4"
                        >
                          <div className="text-white font-medium mb-3 flex justify-between items-center">
                            <span className="flex items-center">
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-5 w-5 mr-2"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"
                                />
                              </svg>
                              {res}p Quality
                            </span>
                            <span className="bg-gray-700 text-xs py-1 px-2 rounded">
                              MP4
                            </span>
                          </div>
                          <div className="grid grid-cols-2 gap-2">
                            <button
                              onClick={() => handlePreviewVideo(res, index)}
                              className={`py-2 px-3 ${
                                activePreview === index
                                  ? "bg-indigo-700"
                                  : "bg-indigo-600 hover:bg-indigo-700"
                              } text-white rounded-md text-center transition duration-150 flex items-center justify-center`}
                            >
                              {activePreview === index && !previewUrl ? (
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                              ) : (
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  className="h-4 w-4 mr-1"
                                  fill="none"
                                  viewBox="0 0 24 24"
                                  stroke="currentColor"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                                  />
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                                  />
                                </svg>
                              )}
                              Preview
                            </button>
                            <a
                              href={getDownloadUrl("mp4", res)}
                              className="py-2 px-3 bg-primary hover:bg-red-700 text-white rounded-md text-center transition duration-150 flex items-center justify-center"
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-4 w-4 mr-1"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                                />
                              </svg>
                              Download
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Searchbar;
