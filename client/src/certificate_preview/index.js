import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
import 'bootstrap/dist/css/bootstrap.css';

const certificatePreview = document.getElementById('certificate_preview');

if (certificatePreview) ReactDOM.render(<React.StrictMode><App /></React.StrictMode>, certificatePreview);
