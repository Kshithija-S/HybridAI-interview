import Table from "./Table/Table";
import { useEffect } from "react";
import useGetUsers from "../hooks/useGetUsers";

const UsersTable = () => {
  const { loading, error, userData, fetchUsers } = useGetUsers();

  useEffect(() => {
    (async () => await fetchUsers())();
  }, [fetchUsers]);

  const columns = [
    {
      id: 1,
      field: "name",
      header: "Name",
      props: {
        sortable: true,
      },
    },
    {
      id: 2,
      field: "username",
      header: "Username",
    },
    {
      id: 3,
      field: "email",
      header: "Email",
    },
    {
      id: 4,
      field: "address.city",
      header: "City",
      props: {
        filter: true,
      },
    },
  ];

  if (error) {
    return <div>{error}</div>;
  }

  return <Table data={userData} columns={columns} loading={loading} />;
};

export default UsersTable;
