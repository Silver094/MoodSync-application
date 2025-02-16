import React from 'react';

const PlaylistPlayer = ({ playlistEmbedUrl }) => {
  return (
    <div className="mt-4">
      <h4>Now Playing</h4>
      <iframe
        src={playlistEmbedUrl}
        width="100%"
        height="380"
        frameBorder="0"
        allowtransparency="true"
        allow="encrypted-media"
        title="Spotify Playlist"
      ></iframe>
    </div>
  );
};

export default PlaylistPlayer;
