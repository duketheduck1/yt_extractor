import { FormEvent, useState } from 'react';
import axios from 'axios';
const Searchbar = ({ onMetadataReceived }) => {
    const [url, setUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async(e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post('http://localhost:8000/api/load-meta-data/', {
                url:url
            });
            onMetadataReceived(response.data);
            
        } catch(err) {
            setError(err.response?.data?.error || 'Failed to fetch video info');
        } finally {
            setLoading(false);
        }
    };

    return (
        
        <form className='flex flex-wrap gap-4 mt-12 border-2 border-red-500'>
            <input type='text' value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Paste Youtube URL here" className ='search-input'/>
            <button 
                type="submit"
                disabled={loading}
                className="search-btn"
            >
                {loading? 'Loading...': 'Search'}
            </button>
            {error && <p className='test-red-500 mt-2'>{error}</p>}
        </form>
    );
};

export default Searchbar;