import React from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import PropTypes from "prop-types";
import "./table.css";

const Table = ({ data, columns = [], loading }) => {
  return (
    <DataTable value={data} loading={loading}>
      {columns.map((column) => (
        <Column
          key={column.id}
          field={column.field}
          header={column.header}
          className="column"
          {...column.props}
        ></Column>
      ))}
    </DataTable>
  );
};

Table.propTypes = {
  data: PropTypes.array,
  columns: PropTypes.array,
  loading: PropTypes.bool,
};

export default Table;
