import SearchBar from "../components/SearchBar";
import Header from "../components/Header";
import { AppContext } from "../context/AppContext";
import { useContext } from "react";
import "./Home.css";
import { useEffect } from "react";
import useAxios from "../hooks/useAxios";

const Home = () => {
  const { user, setUser } = useContext(AppContext);
  const { fetchData } = useAxios();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const fetchUserData = async (token) => {
        try {
          const {data} = await fetchData({
            method: "GET",
            url: "profile",
            options: {},
            auth: true,
          });
          return data;
        } catch (error) {
          console.error("Error fetching user data:", error);
          return null;
        }
      };
      console.log("Fetching user data...");

      const data=fetchUserData(token);
      console.log("data",data);
      
    }
  }, []);
  return (
    <div className="home">
      <Header />
      <div className="m-3">
        <h3 style={{ color: "white" }}>Search for a song</h3>
        <SearchBar />
      </div>
    </div>
  );
};
export default Home;
