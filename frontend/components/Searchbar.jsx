import { FormEvent, useState } from 'react';
import axios from 'axios';
import PreviewVideo from './PreviewVideo';

const Searchbar = () => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [isLoading, setIsLoading] = useState(false); 
    const [error, setError] = useState('');
    const [videoData, setVideoData] = useState(null);


    const handleSubmit = async(e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post(
              'http://localhost:8000/api/load-meta-data/',
              { url }
            );
            if (response.status === 200) {
              setVideoData(response.data);
            } else {
              console.error('Error fetching video data:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching video data:', error);
            setError(error.response?.data?.error || 'Failed to fetch video info');
        } finally {
            setLoading(false);
            setIsLoading(false);
        }
    };

    return (
        <div className="main">
            <form 
                onSubmit={(e) => handleSubmit(e)}
                className='flex flex-wrap gap-4 mt-12 border-2 border-red-500'
            >
                <input 
                    type='text' 
                    value={url} 
                    onChange={(e) => setUrl(e.target.value)} placeholder="Paste Youtube URL here" className ='search-input'/>
                <button 
                    type="submit"
                    disabled={loading}
                    className="search-btn"
                >
                    {loading? 'Loading...': 'Search'}
                </button>
                {error && <p className='test-red-500 mt-2'>{error}</p>}
            </form>
            {isLoading && (
                <div className='flex justify-center items-center py-4'>
                    <div className="w-8 h-8 border-4 border-red-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            )}
            {/* videoData if and not if exist */}
            <div className='container-details flex flex-row'>
                {videoData && (
                    <div className="w-full">
                        <div className="flex-1 bg-white shadow-md rounded p-4">
                        <h4 className="text-xl font-bold mb-4">Video Details</h4>
                        <p><strong>Title:</strong> {videoData.title}</p>
                        <p><strong>Duration:</strong> {videoData.duration}</p>
                        <p><strong>Views:</strong> {videoData.views}</p>
                        <p><strong>Uploader:</strong> {videoData.uploader}</p>
                        <p><strong>URL:</strong> {videoData.url}</p>
                        </div>
                    </div>
                )}
                <div className="list-center">
                    {videoData && videoData.resolution && (
                        <div>
                            <div className='flex flex-row gap-4'>
                                <a href={"http://localhost:8000/api/download/f"+url.split('v=')[1]+"0125.mp3/"}>Audio mp3</a>
                                
                            </div>
                        {videoData.resolution.map((res, index) => (
                            
                            <div key={index} className='flex flex-row gap-4'>
                            <a href={"http://localhost:8000/api/download/f"+url.split('v=')[1]+(res.toString().length==3?"0":"") +res+".mp4/"}>{res}p</a>
                            <PreviewVideo 
                                url={"http://localhost:8000/api/preview-video/f"+url.split('v=')[1]+(res.toString().length==3?"0":"") +res+".mp4/"}
                                res={""+res}
                            />
                            </div>
                        ))}
                        </div>
                    )}
                </div>
            </div>
            
        </div>
        
    );
};

export default Searchbar;