import { useCallback, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

const useRegisterUser = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState(localStorage.getItem("user"));

  const registerUser = useCallback(async (data, callback) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}user/register/`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const userData = await response.json();
      if (userData?.error) {
        setError(userData?.error);
        return;
      }
      localStorage.setItem("token", userData?.tokens);
      localStorage.setItem("user", JSON.stringify(userData?.user));
      setUserData(userData?.user);
      callback();
    } catch (error) {
      setError(error?.message);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    userData,
    registerUser,
  };
};

export default useRegisterUser;
