import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Callback() {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');

    if (code) {
      fetch(`http://localhost:8888/callback?code=${code}`)
        .then(response => response.json())
        .then(data => {
          localStorage.setItem('token', data.access_token);
          navigate('/player');
        });
    }
  }, [navigate]);

  return <div>Loading...</div>;
}

export default Callback;