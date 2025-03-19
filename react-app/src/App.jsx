import React, { useState } from "react";
import "./App.css";
import UsersTable from "./components/UsersTable";
import { Button } from "primereact/button";
import RegisterModal from "./components/Register/RegisterModal";

function App() {
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <div>
      <div style={{ display: "flex", gap: "10px" }}>
        {user ? (
          <div>Hello {user?.full_name},</div>
        ) : (
          <>
            <Button
              label="Register"
              className="register-btn"
              onClick={() => setIsRegisterModalOpen(true)}
            />
            <Button
              label="Login"
              className="register-btn"
              onClick={() => setIsLoginModalOpen(true)}
            />
          </>
        )}
      </div>
      <RegisterModal
        isOpen={isRegisterModalOpen || isLoginModalOpen}
        onClose={() => {
          setIsRegisterModalOpen(false);
          setIsLoginModalOpen(false);
        }}
        isLogin={isLoginModalOpen}
      />
      <UsersTable />
    </div>
  );
}

export default App;
