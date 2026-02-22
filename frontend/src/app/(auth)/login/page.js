"use client";
import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/auth/login', { email, password });
            
            // Save Token and User Info
            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            // router.push('/dashboard'); // Redirect to dashboard
            window.location.href = '/dashboard'; // Force reload to update auth state
            
        } catch (err) {
            alert(err.response?.data?.detail || "Login Failed");
        } finally  {
            setEmail('');
            setPassword('');
        }
    };

    return (
        <>
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-4">
                    <div className="card shadow">
                        <div className="card-body">
                            <h3 className="card-title text-center mb-4">Login</h3>
                            <form onSubmit={handleLogin}>
                                <div className="mb-3">
                                    <label className="form-label">Email</label>
                                    <input type="email" className="form-control" 
                                        onChange={(e) => setEmail(e.target.value)} required />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Password</label>
                                    <input type="password" className="form-control" 
                                        onChange={(e) => setPassword(e.target.value)} required />
                                </div>
                                <button type="submit" className="btn btn-primary w-100">Sign In</button>
                            </form>
                            <p className="mt-3 text-center">
                                Don't have an account? <a href="/signup">Sign Up</a>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}