import PropTypes from "prop-types";
import React from "react";
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";
import "./register.css";

const RegisterForm = ({ formData, handleChange, handleSubmit, onClose }) => {
  return (
    <form onSubmit={handleSubmit} className="p-fluid">
      <div className="field">
        <label htmlFor="username">Username</label>
        <InputText
          id="username"
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
      </div>
      <div className="field">
        <label htmlFor="email">Email</label>
        <InputText
          id="email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div className="field">
        <label htmlFor="name">Full Name</label>
        <InputText
          id="name"
          type="text"
          name="full_name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div className="field">
        <label htmlFor="password">Password</label>
        <InputText
          id="password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div className="flex justify-content-end mt-4">
        <Button type="submit" label="Register" className="mr-2" />
        <Button
          type="button"
          label="Cancel"
          className="p-button-outlined"
          onClick={onClose}
        />
      </div>
    </form>
  );
};

RegisterForm.propTypes = {
  formData: PropTypes.object.isRequired,
  handleChange: PropTypes.func.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default RegisterForm;
