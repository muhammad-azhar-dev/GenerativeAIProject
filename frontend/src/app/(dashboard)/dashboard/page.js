"use client";
import { useState, useEffect } from 'react';
import axios from 'axios';
import ProtectedRoute from '@/components/ProtectedRoute';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [file, setFile] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    // Fetch user history on load
    useEffect(() => {
        const userData = JSON.parse(localStorage.getItem('user'));
        setUser(userData);
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:8000/my-history', {
            headers: { Authorization: `Bearer ${token}` }
        });
        setHistory(res.data);
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        setLoading(true);
        const token = localStorage.getItem('token');
        const userId = user.id;
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('owner_id', userId);

        try {
            await axios.post('http://localhost:8000/generate', formData, {
                headers: { 
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${token}` 
                }
            });
            fetchHistory(); // Refresh the list
        } catch (err) {
            alert(err.response?.data?.detail || "Error generating content");
        } finally {
            setLoading(false);
        }
    };

    return (
        <ProtectedRoute>
            <>
        <div className="container">
            <h2>Welcome back {user?.username || 'User'}!</h2>
            <div className="card p-4 mb-5 bg-light">
                <form onSubmit={handleUpload}>
                    <div className="mb-3">
                        <label className="form-label">Upload Image or PDF</label>
                        <input type="file" className="form-control" accept=".jpg,.jpeg,.png,.pdf" 
                            onChange={(e) => setFile(e.target.files[0])} required />
                    </div>
                    <button type="submit" className="btn btn-success" disabled={loading}>
                        {loading ? 'Processing with Gemini...' : 'Analyze File'}
                    </button>
                </form>
            </div>

            <h3>Your History</h3>
            <div className="row">
                {history.map((item) => (
                    <div className="col-md-6 mb-3" key={item.id}>
                        <div className="card h-100">
                            <div className="card-body overflow-auto flex-grow-1 mt-auto" style={{ height: "450px",whiteSpace: "pre-wrap" }}>
                                <h5 className="text-black">File: {item.file_path}</h5>
                                <hr />
                                <p className="card-text">{item.gemini_output}...</p>
                                <br />
                                <small className="text-muted">File: {item.file_path}</small>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
        </>
        </ProtectedRoute>
    );
}