// components/Sidebar.js
"use client";
import Link from "next/link";

export default function Sidebar() {
  return (
    <div 
      className="offcanvas offcanvas-start text-bg-light" 
      tabIndex="-1" 
      id="sidebarMenu" 
      aria-labelledby="sidebarMenuLabel"
      style={{ width: '280px' }}
    >
      <div className="offcanvas-header border-bottom">
        <h5 className="offcanvas-title" id="sidebarMenuLabel">Menu</h5>
        <button 
          type="button" 
          className="btn-close" 
          data-bs-dismiss="offcanvas" 
          aria-label="Close"
        ></button>
      </div>
      
      <div className="offcanvas-body">
        <ul className="nav nav-pills flex-column mb-auto">
          <li className="nav-item mb-2">
            <Link href="/dashboard" className="nav-link active">🏠 Dashboard</Link>
          </li>
          <li className="nav-item mb-2">
            <Link href="/userprofile" className="nav-link link-dark">👤 User Profile</Link>
          </li>
          <li className="nav-item mb-2">
            <Link href="/allusers" className="nav-link link-dark">👥 Users</Link>
          </li>
          <li className="nav-item mb-2">
            <Link href="/billing" className="nav-link link-dark">💳 Billing</Link>
          </li>
        </ul>
        <hr />
        <div className="small text-muted">Gemini 3 Flash Project</div>
      </div>
    </div>
  );
}