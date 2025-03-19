import { useCallback, useState } from "react";

const useGetUsers = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState([]);

  const apiUrl = "https://jsonplaceholder.typicode.com/users";

  const fetchUsers = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch(apiUrl, {
        method: "GET",
      });

      const userData = await response.json();
      userData.sort((a, b) => a.name.localeCompare(b.name));
      setUserData(userData);
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
    fetchUsers,
  };
};

export default useGetUsers;
