import SearchBar from "../components/SearchBar";
import Header from "../components/Header";

import "./Home.css";
const Home = () => {
  return (
    <div className="home">
      <Header/>
      <div className="m-3">
        <h3 style={{ color: "white" }}>Search for a song</h3>
        <SearchBar />
      </div>
    </div>
  );
};
export default Home;
