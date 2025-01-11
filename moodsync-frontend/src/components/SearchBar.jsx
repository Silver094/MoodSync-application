import React, { useState } from "react";
import useAxios from "../hooks/useAxios";

function SearchBar() {
  const [searchValue, setSearchValue] = useState("");
  const { fetchData } = useAxios();
  // Call your API here
  const handleSearch = async () => {
    try {
      const response = await fetchData({
        method: "POST",
        url: "moods",
        options: {
          data: {searchValue},
          headers: {
            "Content-Type": "application/json",
          },
        },
        auth:false
      });
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const handleSearchClick = () => {
    if (searchValue === "") {
      alert("Please enter a search term");
      return;
    }
    handleSearch();
    console.log("Search button clicked");
  };

  return (
    <div
      className=""
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <input
          type="text"
          className="form-control"
          placeholder="How are you feeling?"
          aria-label="How are you feeling?"
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearchClick();
            }
          }}
        />
        <button
          type="button"
          className="btn btn-primary mt-2"
          style={{
            width: "fit-content",
            backgroundColor: "gray",
            border: "none",
          }}
          onClick={handleSearchClick}
        >
          SEARCH
        </button>
      </div>
    </div>
  );
}
export default SearchBar;
