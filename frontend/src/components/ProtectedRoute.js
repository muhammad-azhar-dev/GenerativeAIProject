"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ProtectedRoute({ children }) {
    const router = useRouter();
    const [verified, setVerified] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("token");
        
        if (!token) {
            // No token? Send them to login
            router.replace("/login");
        } else {
            // Token exists? Let them in
            setVerified(true);
        }
    }, [router]);

    if (!verified) {
        // Show a full-screen loader while checking the token
        return (
            <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return children;
}