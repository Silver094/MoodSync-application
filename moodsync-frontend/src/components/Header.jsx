import React from "react";
import { useContext } from "react";
import { AppContext } from "../context/AppContext";
import { useNavigate } from "react-router-dom";

function Header() {
  const { user } = useContext(AppContext);
  const navigate=useNavigate();
  return (
    <div className="home_header d-flex align-items-center justify-content-between p-3 bg-dark">
      {/* Logo and moodSync */}
      <div className="d-flex flex-column align-items-center justify-content-center">
        <img src="icons/logo.png" alt="logo" height={28} />
        <p className="text-white  mb-0" style={{ fontSize: "3px" }}>
          moodsync
        </p>
      </div>

      {/* Profile Dropdown */}
      <div className="dropdown">
        <button
          className="btn dropdown-toggle"
          type="button"
          id="profileDropdown"
          style={{
            backgroundColor: "transparent",
            color: "white",
            border: "none",
            outline: "none",
          }}
          data-bs-toggle="dropdown"
          aria-expanded="false"
          disabled={!user}
          ondisabled="this.style.display='none'"
        >
          {user?.display_name?.split(" ")[0] ?? "moodSync"}
        </button>
        <ul
          className="dropdown-menu dropdown-menu-dark"
          aria-labelledby="profileDropdown"
        >
          <li>
            <a className="dropdown-item" 
            onClick={() => {
              navigate("/profile");
            }}
            >
              Profile
            </a>
          </li>
          <li>
            <hr className="dropdown-divider" />
          </li>
          <li>
            <a
              className="dropdown-item"
              onClick={() => {
                localStorage.removeItem("token");
                window.location.href = "/";
              }}
            >
              Logout
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default Header;
