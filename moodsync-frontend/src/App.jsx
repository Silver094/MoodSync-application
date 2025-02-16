import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import Callback from './components/Callback'; // This handles the OAuth callback
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/spotify/callback" element={<Callback />} />
          
          {/* <Route path="*" element={<Navigate to="/" />} /> Redirect to "/" for any other route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
