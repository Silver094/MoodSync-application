import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const spotifyToken = params.get('spotifyToken');
    const error = params.get('message');

    if (error) {
      setError(error);
      setTimeout(() => navigate('/'), 3000);
      return;
    }

    if (!token || !spotifyToken) {
      setError('Invalid authentication response');
      setTimeout(() => navigate('/'), 3000);
      return;
    }

    try {
      // Store tokens
      localStorage.setItem('token', token);
      localStorage.setItem('spotifyToken', spotifyToken);
      
      // Redirect to dashboard
      navigate('/');
    } catch (err) {
      setError('Failed to store authentication data');
      setTimeout(() => navigate('/'), 3000);
    }
  }, [navigate]);

  if (error) {
    return (
      <div className="alert alert-danger">
        Authentication Error: {error}
        <br />
        Redirecting to home...
      </div>
    );
  }

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ height: '200px' }}>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
};

export default Callback;