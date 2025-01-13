import React from "react";
import "./Profile.css";
import { useContext } from "react";
import { AppContext } from "../context/AppContext";

const Profile = () => {
  const { user } = useContext(AppContext);

  return (
    <div className="profile-container">
      <div className="profile-card">
        {/* Profile Picture */}
        <div className="profile-image">
          {user?.images.length > 0 ? (
            <img src={user?.images[0].url} alt={`${user?.display_name}'s profile`} />
          ) : (
            <div className="placeholder-image">No Image</div>
          )}
        </div>

        {/* Profile Details */}
        <div className="profile-details">
          <h1>{user?.display_name}</h1>
          <p><strong>Email:</strong> {user?.email}</p>
          <p><strong>Country:</strong> {user?.country}</p>
          <p>
            <strong>Subscription:</strong> {user?.product}
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
