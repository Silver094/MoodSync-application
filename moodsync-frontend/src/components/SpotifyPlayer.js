import React, { useEffect, useState } from 'react';

const SpotifyPlayer = ({ playlistUri }) => {
  const [player, setPlayer] = useState(null);
  const [deviceId, setDeviceId] = useState(null);
  const [notPremium, setNotPremium] = useState(false);
  
  // IMPORTANT: Make sure you store your Spotify access token under "spotifyToken"
  const spotifyToken = localStorage.getItem('spotifyToken'); 

  // For debugging, log the token
  useEffect(() => {
    console.log("Spotify Token:", spotifyToken);
  }, [spotifyToken]);

  // Load the Spotify Web Playback SDK
  useEffect(() => {
    if (!document.getElementById('spotify-player-script')) {
      const script = document.createElement("script");
      script.id = "spotify-player-script";
      script.src = "https://sdk.scdn.co/spotify-player.js";
      script.async = true;
      document.body.appendChild(script);
    }

    window.onSpotifyWebPlaybackSDKReady = () => {
      const spotifyPlayer = new window.Spotify.Player({
        name: 'MoodSync Player',
        getOAuthToken: (cb) => { cb(spotifyToken); },
        volume: 0.5,
      });

      // Listen for errors
      spotifyPlayer.addListener('initialization_error', ({ message }) =>
        console.error("Initialization Error:", message)
      );
      spotifyPlayer.addListener('authentication_error', ({ message }) =>
        console.error("Authentication Error:", message)
      );
      spotifyPlayer.addListener('account_error', ({ message }) => {
        console.error("Account Error:", message);
        setNotPremium(true);
      });
      spotifyPlayer.addListener('playback_error', ({ message }) =>
        console.error("Playback Error:", message)
      );

      // When ready, get the device ID
      spotifyPlayer.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
        setDeviceId(device_id);
      });

      spotifyPlayer.connect().then(success => {
        if (success) {
          console.log("Spotify Web Playback SDK connected successfully!");
        } else {
          console.error("Spotify Web Playback SDK failed to connect.");
        }
      });
      setPlayer(spotifyPlayer);
    };
  }, [spotifyToken]);

  // Transfer playback to the Web Playback SDK device (for Premium users)
  const transferPlayback = async () => {
    if (!deviceId) return;
    try {
      const response = await fetch('https://api.spotify.com/v1/me/player', {
        method: 'PUT',
        body: JSON.stringify({
          device_ids: [deviceId],
          play: true
        }),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${spotifyToken}`
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Transfer playback error:", errorData);
      }
    } catch (error) {
      console.error("Transfer playback exception:", error);
    }
  };

  useEffect(() => {
    if (deviceId && !notPremium) {
      transferPlayback();
    }
  }, [deviceId, spotifyToken, notPremium]);

  // Function to trigger playback via the SDK
  const playPlaylist = async () => {
    if (!deviceId) return;
    try {
      const response = await fetch(`https://api.spotify.com/v1/me/player/play?device_id=${deviceId}`, {
        method: 'PUT',
        body: JSON.stringify({ context_uri: playlistUri }),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${spotifyToken}`
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Play playlist error:", errorData);
      }
    } catch (error) {
      console.error("Play playlist exception:", error);
    }
  };

  // Helper: Convert Spotify URI to a URL for fallback redirection
  const getPlaylistUrl = () => {
    const parts = playlistUri.split(':');
    const playlistId = parts[2];
    return `https://open.spotify.com/playlist/${playlistId}`;
  };

  return (
    <div>
      {notPremium ? (
        <div className="alert alert-warning mt-3">
          Full in‑app playback is available for Premium users only.
          <br />
          <a
            href={getPlaylistUrl()}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary mt-2"
          >
            Open Playlist in Spotify
          </a>
        </div>
      ) : (
        <div>
          <button onClick={playPlaylist} className="btn btn-primary mt-3">
            Play Full Playlist
          </button>
        </div>
      )}
    </div>
  );
};

export default SpotifyPlayer;
