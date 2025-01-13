import React from "react";
import "./Profile.css";
import { useContext } from "react";
import { AppContext } from "../context/AppContext";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { user } = useContext(AppContext);
  const navigate = useNavigate(); // Hook for navigation

  return (
    <div className="profile-container ">
      {/* Back Button */}
      <div className="back-button" style={{position:'fixed', top:30,left:30 ,background:'none'}} onClick={() => navigate(-1)}>
        <span
        style={{ width: 100, height: 100, background:"none"}}
        >&larr;</span> 
      </div>

      <div className="profile-card">
        {/* Profile Picture */}
        <div className="profile-image">
          {user?.images.length > 0 ? (
            <img
              src={user?.images[0].url}
              alt={`${user?.display_name}'s profile`}
            />
          ) : (
            <div className="placeholder-image">No Image</div>
          )}
        </div>

        {/* Profile Details */}
        <div className="profile-details">
          <h1>{user?.display_name}</h1>
          <p>
            <strong>Email:</strong> {user?.email}
          </p>
          <p>
            <strong>Country:</strong> {user?.country}
          </p>
          <a
            href={user?.external_urls.spotify}
            target="_blank"
            rel="noopener noreferrer"
            className="spotify-link"
          >
            View on Spotify
          </a>
        </div>
      </div>
    </div>
  );
};

export default Profile;
