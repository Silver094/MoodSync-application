import Header from "../components/Header";
import "./Login.css";
function Login() {
  const handleSpotifyLogin = () => {
    window.location.href = "http://localhost:8888/login";
  };
  return (
    <div>
      <Header />
      <div className="login">
        <h2>Login</h2>
        <h5>using</h5>
        <button
          type="button"
          className="btn btn-primary  mt-3 btn-lg"
          style={{
            backgroundColor: "green",
            border: "none",
            borderRadius: "40px",
            paddingLeft: "40px",
            paddingRight: "40px",
            fontWeight: "600",
          }}
          onClick={handleSpotifyLogin}
        >
          Spotify
        </button>
      </div>
    </div>
  );
}
export default Login;
