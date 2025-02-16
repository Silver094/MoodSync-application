import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    const spotifyToken = params.get('spotifyToken');
    if (token) {
      localStorage.setItem('token', token);
    }
    if (spotifyToken) {
      localStorage.setItem('spotifyToken', spotifyToken);
    }
    if (token) {
      navigate('/');
    }
  }, [navigate]);

  return <div>Logging you in...</div>;
};

export default Callback;
