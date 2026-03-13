"use client";
import { useState, useEffect } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function UserProfile() {
  // States for Profile Section
  const [username, setUsername] = useState("John Doe");
  const [email, setEmail] = useState("john@example.com");

  // States for Password Section
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  // show hide password
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    // Yahan aap FastAPI ki '/profile' API call karenge token ke saath
    getProfileData();
  }, []);

  const getProfileData = async () => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const user = JSON.parse(userData);
      setUsername(user.username);
      setEmail(user.email);
    }
  }

  const handleUpdateProfile = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      alert("No token found. Please log in.");
    }
    const response = fetch("http://localhost:8000/users/update-profile", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ username, email }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to update profile");
        }
        return res.json();
      })
      .then((data) => {
        alert("Profile updated successfully!");
      })
      .catch((error) => {
        alert(error.message);
      });
  };

  const handleChangePassword = (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    if (!token) {
      alert("No token found. Please log in.");
      return;
    }
    const response = fetch("http://localhost:8000/users/change-password", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ old_password: oldPassword, password: newPassword }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to change password");
        }
        return res.json();
      })
      .then((data) => {
        alert("Password changed successfully!");
        setOldPassword("");
        setNewPassword("");
      })
      .catch((error) => {
        alert(error.message);
      });
  };

  const handleToggleShowPassword = () => {
    setShowPassword(!showPassword);
  }

  return (
    <ProtectedRoute>
      <>
    <div className="container mt-4">
      <h2 className="mb-4">User Settings</h2>
      <div className="row">
        
        {/* Section 1: Update Profile */}
        <div className="col-md-6 mb-4">
          <div className="card shadow-sm">
            <div className="card-header bg-primary text-white">
              <h5 className="mb-0">Personal Information</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleUpdateProfile}>
                <div className="mb-3">
                  <label className="form-label">Full Name</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Email Address</label>
                  <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary">
                  Update Profile
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Section 2: Change Password */}
        <div className="col-md-6 mb-4">
          <div className="card shadow-sm border-danger">
            <div className="card-header bg-danger text-white">
              <h5 className="mb-0">Security & Password</h5>
            </div>
            <div className="card-body">
              <form onSubmit={handleChangePassword}>
                <div className="mb-3">
                  <label className="form-label">Old Password</label>
                  <input
                    type={showPassword ? "text" : "password"}
                    className="form-control"
                    placeholder="Enter current password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">New Password</label>
                  <input
                    type={showPassword ? "text" : "password"}
                    className="form-control"
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    required
                  />
                </div>
                <div className="form-check">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      value=""
                      id="flexCheckDefault"
                      checked={showPassword}
                      onChange={()=>{setShowPassword(!showPassword)}}
                      onClick={handleToggleShowPassword}
                    />
                    <label className="form-check-label" htmlFor="flexCheckDefault">
                      Show Password
                    </label>
                  </div>
                <button type="submit" className="btn btn-outline-danger">
                  Change Password
                </button>
              </form>
            </div>
          </div>
        </div>

      </div>
    </div>
    </>
    </ProtectedRoute>
  );
}