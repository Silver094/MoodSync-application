import "./Greeting.css";
import Logo from "../components/Logo";
import { useNavigate } from "react-router-dom";

function Greeting() {
  const navigate = useNavigate();
  return (
    <div className="body">
      <h1>Welcome to MoodSync!</h1>
      <Logo width={"180px"} />

      <div className="mt-5">
        {/* <div className="border-top border-white border-2" /> */}
        <button
          type="button"
          className="btn btn-primary mt-2 btn-lg"
          style={{
            backgroundColor: "gray",
            border: "none",
            borderRadius: "10px",
            fontWeight: "600",
          }}
          onClick={() => navigate("/login")}
        >
          Get Started
        </button>
      </div>
    </div>
  );
}
export default Greeting;
