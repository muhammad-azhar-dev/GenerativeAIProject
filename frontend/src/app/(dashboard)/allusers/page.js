"use client";
import { useState, useEffect } from "react";
import ProtectedRoute from "@/components/ProtectedRoute";

export default function UsersList() {
  // Dummy data (Baad mein ye FastAPI se ayega)
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // 1. LocalStorage se token nikalna (Login ke waqt save kiya hoga)
        const token = localStorage.getItem("token"); 

        // 2. API Call karna
        const response = await fetch("http://127.0.0.1:8000/users/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` // <--- Token yahan ja raha hai
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch users or Unauthorized");
        }

        const data = await response.json();
        setUsers(data); // State update karna
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <ProtectedRoute>
      {loading && <div className="p-5">Loading users...</div>}
      {error && <div className="alert alert-danger m-5">Error: {error}</div>}
      <>
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Registered Users</h2>
      </div>

      <div className="card shadow-sm">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead className="table-light">
                <tr>
                  <th className="ps-4">#ID</th>
                  <th>User Name</th>
                  <th>Email Address</th>
                </tr>
              </thead>
              <tbody>
                {users?.map((user) => (
                  <tr key={user.id}>
                    <td className="ps-4 text-muted">{user.id}</td>
                    <td><strong>{user.username}</strong></td>
                    <td>{user.email}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {users.length === 0 && (
        <div className="text-center mt-4">
          <p className="text-muted">No users found in the database.</p>
        </div>
      )}
    </div>
    </>
    </ProtectedRoute>
  );
}