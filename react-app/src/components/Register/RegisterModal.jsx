import { useState } from "react";
import { Dialog } from "primereact/dialog";
import useRegisterUser from "../../hooks/useRegisterUser";
import RegisterForm from "./RegisterForm";
import PropTypes from "prop-types";
import "./register.css";
import useLoginUser from "../../hooks/useLoginUser";

const RegisterModal = ({ isOpen, onClose, isLogin = false }) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    full_name: "",
    password: "",
  });
  const { loading, error, registerUser } = useRegisterUser();
  const {
    loading: loginLoading,
    error: loginError,
    loginUser,
  } = useLoginUser();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    !isLogin
      ? await registerUser({ ...formData }, onClose)
      : await loginUser({ ...formData }, onClose);
  };

  const renderLoadingOrError = () => {
    return loading || loginLoading ? (
      <div> Loading...</div>
    ) : (
      (error || loginError) && (
        <div className="p-error">{error || loginError}</div>
      )
    );
  };

  return (
    <Dialog
      header={isLogin ? "Login" : "Register"}
      visible={isOpen}
      onHide={onClose}
      className="custom-dialog"
    >
      {loading || error || loginLoading || loginError ? (
        renderLoadingOrError()
      ) : (
        <RegisterForm
          formData={formData}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          onClose={onClose}
        />
      )}
    </Dialog>
  );
};

RegisterModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  isLogin: PropTypes.bool,
};

export default RegisterModal;
