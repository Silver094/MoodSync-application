import React, { useEffect, useState } from "react";

const Profile = () => {
  // Local unified profile from your backend (created/updated via Spotify SSO)
  const [localProfile, setLocalProfile] = useState(null);
  // Optionally, fetch the latest Spotify profile details directly from Spotify
  const [spotifyProfile, setSpotifyProfile] = useState(null);
  const token = localStorage.getItem("token"); // MoodSync JWT from Spotify login
  const spotifyToken = localStorage.getItem("spotifyToken"); // Stored Spotify access token

  // Fetch the unified MoodSync profile from your backend
  const baseUrl = process.env.REACT_APP_API_URL;
  useEffect(() => {
    fetch(baseUrl+"api/profile", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {setLocalProfile(data)
      console.log(data)}
    )

      .catch((err) => console.error("Error fetching local profile:", err));
  }, [token]);

  // Optionally fetch the latest Spotify profile details directly from Spotify
  useEffect(() => {
    if (spotifyToken) {
      fetch("https://api.spotify.com/v1/me", {
        headers: {
          Authorization: `Bearer ${spotifyToken}`,
        },
      })
        .then((res) => res.json())
        .then((data) => setSpotifyProfile(data))
        .catch((err) => console.error("Error fetching Spotify profile:", err));
    }
  }, [spotifyToken]);

  if (!localProfile) {
    return <div>Loading your profile...</div>;
  }

  // Use Spotify data if available; otherwise, fall back to your local profile data.
  const displayName =
    (spotifyProfile && spotifyProfile.display_name) ;
  const email = (spotifyProfile && spotifyProfile.email) ;
  const accountType = (spotifyProfile && spotifyProfile.product) || "standard";
  

  return (
    <div className="container mt-4">
      <h2>User Profile</h2>
      <div className="card p-4">
        <div className="d-flex align-items-center mb-3">
          <div>
            <p>
              <strong>Display Name:</strong> {displayName}
            </p>
            <p>
              <strong>Email:</strong> {email}
            </p>
            <p>
              <strong>Account Type:</strong> {accountType}
            </p>
          </div>
        </div>
        <hr />
        <p>
          <strong>MoodSync Member Since:</strong>{" "}
          {new Date(localProfile.created_at.$date).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
};

export default Profile;
