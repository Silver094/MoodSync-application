import SearchBar from "../components/SearchBar";

import "./Home.css";
const Home = () => {
  return (
    <div className="home">
      <div className="home_header">
        <img src="icons/logo.png" alt="logo" height={28} width={"auto"} />
        <h3 style={{ color: "white" }}>moodSync</h3>
      </div>
      <div className="m-3">
        <h3 style={{ color: "white" }}>Search for a song</h3>
        <SearchBar />
      </div>
    </div>
  );
};
export default Home;
