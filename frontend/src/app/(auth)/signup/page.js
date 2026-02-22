"use client";
import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
    const [formData, setFormData] = useState({ username: '', email: '', password: '' });
    const router = useRouter();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/auth/signup', formData);
            alert("Account created successfully! Please login.");
            // router.push('/login');
            window.location.href = '/login'; // Force reload to update auth state
        } catch (err) {
            alert(err.response?.data?.detail || "Signup failed");
        }
    };

    return (
        <>
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-5">
                    <div className="card border-0 shadow-lg">
                        <div className="card-body p-5">
                            <h2 className="text-center mb-4">Create Account</h2>
                            <form onSubmit={handleSignup}>
                                <div className="mb-3">
                                    <label className="form-label">Username</label>
                                    <input type="text" className="form-control" 
                                        onChange={(e) => setFormData({...formData, username: e.target.value})} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input type="email" className="form-control" 
                                        onChange={(e) => setFormData({...formData, email: e.target.value})} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input type="password" className="form-control" 
                                        onChange={(e) => setFormData({...formData, password: e.target.value})} required />
                                </div>
                                <button type="submit" className="btn btn-primary w-100 py-2">Sign Up</button>
                            </form>
                            <div className="text-center mt-3">
                                <span>Already have an account? <a href="/login">Login</a></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}