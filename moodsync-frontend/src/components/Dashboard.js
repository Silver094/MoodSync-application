import React, { useState } from "react";
import SpotifyPlayer from "./SpotifyPlayer";

function Dashboard() {
  const [situationText, setSituationText] = useState("");
  const [playlistUri, setPlaylistUri] = useState(null);
  const [detectedMood, setDetectedMood] = useState(null);
  const [error, setError] = useState("");
  const baseUrl = process.env.REACT_APP_API_URL;
  // MoodSync JWT token
  const token = localStorage.getItem("token");
  // Spotify token for playback
  const spotifyToken = localStorage.getItem("spotifyToken");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!situationText) {
      setError("Please describe your situation.");
      return;
    }
    try {
      const response = await fetch(baseUrl+"/api/recommendation/from-situation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ situation: situationText }),
      });
      const data = await response.json();
      if (response.ok) {
        setDetectedMood(data.detected_mood);
        // Expecting a Spotify URI from the backend (e.g., "spotify:playlist:...")
        setPlaylistUri(data.playlist_uri);
      } else {
        setError(data.error || "Error fetching recommendation");
      }
    } catch (err) {
      setError("An error occurred: " + err.message);
    }
  };


  return (
    <div>
      <div className="d-flex justify-content-between align-items-center">
        <h2>Dashboard</h2>
      </div>

      <div className="card p-4 mt-4">
        <h4>Describe Your Situation</h4>
        {error && <div className="alert alert-danger">{"Please Login!"}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <textarea
              className="form-control"
              placeholder="Describe your current situation..."
              value={situationText}
              onChange={(e) => setSituationText(e.target.value)}
              rows="4"
              required
            ></textarea>
          </div>
          <button type="submit" className="btn btn-primary">
            Get Recommendation
          </button>
        </form>
      </div>

      {detectedMood && (
        <div className="mt-4">
          <h5>Detected Mood: {detectedMood}</h5>
        </div>
      )}

      {/* Show Spotify login if no token is present */}
      {/* {!spotifyToken && <SpotifyAuth />} */}

      {/* If a Spotify token exists, allow account switching */}
      {/* {spotifyToken && <SwitchSpotifyButton />} */}

      {/* Show the SpotifyPlayer if the user is authenticated with Spotify and we have a playlist URI */}
      {spotifyToken && playlistUri && (
        <SpotifyPlayer playlistUri={playlistUri} />
      )}
    </div>
  );
}

export default Dashboard;
