import React, { createContext, useState } from "react";

export const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [moods, setMoods] = useState([]);
  const [user, setUser] = useState({ name: "", isLoggedIn: false });
  const [theme, setTheme] = useState("light");
  // Add other global states here

  return (
    <AppContext.Provider
      value={{
        moods,
        setMoods,
        user,
        setUser,
        theme,
        setTheme,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
