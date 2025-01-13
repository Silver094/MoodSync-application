import SearchBar from "../components/SearchBar";
import Header from "../components/Header";
import { AppContext } from "../context/AppContext";
import { useContext } from "react";
import "./Home.css";
import { useEffect } from "react";
import useAxios from "../hooks/useAxios";

const Home = () => {
  const { setUser } = useContext(AppContext);
  const { fetchData } = useAxios();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      const fetchUserData = async () => {
        try {
          const { data } = await fetchData({
            method: "GET",
            url: "profile",
            options: {},
            auth: true,
          });
          return data; // Resolved user data
        } catch (error) {
          console.error("Error fetching user data:", error);
          return null;
        }
      };

      const loadUserData = async () => {
        console.log("Fetching user data...");
        const data = await fetchUserData(); // Wait for the promise to resolve
        console.log("Data", data);
        if (data) {
          setUser(data); // Set user data in the context
        }
        console.log("User data fetched:", data); // Log resolved data
      };

      loadUserData(); // Call the async function
    }
  }, [setUser]);

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
