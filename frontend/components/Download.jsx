import { FormEvent, useState } from 'react';
import axios from 'axios';

const Download = ({ onMetadataReceived }) => {
    const [format, setFormat] = useState('video');
    const [ resolution, setResolution] = useState(MediaMetadata.resolution[0]);
    const [ fileFormat, setFileFormat] = useState(MediaMetadata.resolution[0]);
    const [status, setStatus] = useState('');
    const [loading, setLoading] = useState(false);


    

export default Download;