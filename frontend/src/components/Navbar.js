"use client";
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Navbar() {
    const router = useRouter();

    const handleLogout = () => {
        // 1. Clear the local storage
        localStorage.removeItem('token');
        localStorage.removeItem('user');

        // 2. Redirect to login page
        // router.push('/login');
        window.location.href = '/login';
    };

    return (
        <>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4">
            <div className="container">
                <a className="navbar-brand" href="/dashboard">Gemini Reader</a>
                <ul className='d-flex list-unstyled mx-2 w-100 mb-0'>
                            <li className="nav-item text-light">
                                <Link className="nav-link" href="/dashboard">Dashboard</Link>
                            </li>
                            <li className="nav-item text-light mx-3">
                                <Link className="nav-link" href="/users">Users</Link>
                            </li>
                </ul>
                <div className="d-flex">
                    <button 
                        className="btn btn-outline-light btn-sm" 
                        onClick={handleLogout}
                    >
                        <i className="bi bi-box-arrow-right me-1"></i> Logout
                    </button>
                </div>
            </div>
        </nav>
        </>
    );
}