import { useState } from "react";
import axios from "axios";

const useAxios = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusCode, setStatusCode] = useState(0);

  const baseUrl = process.env.REACT_APP_API_URL;

  const fetchData = async ({ method, url, options, auth }) => {
    try {
      setLoading(true);

      let config = { method, url: baseUrl + url };
      if (options) {
        config = { ...config, ...options };
      }
      if (auth) {
        const token = localStorage.getItem("token");
        if (token) {
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${token}`,
          };
        } else {
          return {
            data: null,
            error: "No token",
            statusCode: 401,
          };
        }
      }
      const response = await axios(config);
      setData(response.data);
      setStatusCode(response.status);
      return { data: response.data, statusCode: response.status, error: null };
    } catch (error) {
      setError(error.response?.data?.message);
      return {
        data: null,
        error: error.response?.data,
        statusCode: error.response ? error.response.status : 500,
      };
    } finally {
      setLoading(false);
    }
  };

  return { data, error, loading, fetchData, statusCode };
};
export default useAxios;
