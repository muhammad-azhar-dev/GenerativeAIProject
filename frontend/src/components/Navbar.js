"use client";
import { useRouter } from "next/navigation";

// components/Navbar.js
export default function Navbar() {
  const router = useRouter();
  const handelLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    router.push("/login");
    window.location.reload();   
  } 
  return (
    <nav className="navbar navbar-dark bg-dark sticky-top">
      <div className="container-fluid">
        {/* Hamburger Icon */}
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="offcanvas" 
          data-bs-target="#sidebarMenu" 
          aria-controls="sidebarMenu"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <a className="navbar-brand ms-2" href="#">AI Document Reader</a>
        
        <button 
            className="btn btn-outline-danger btn-sm" 
            onClick={handelLogout}
          >
            Logout 🚪
          </button>
      </div>
    </nav>
  );
}