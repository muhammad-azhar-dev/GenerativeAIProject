// app/layout.js
"use client"; // Required to initialize Bootstrap JS
import "bootstrap/dist/css/bootstrap.min.css";
import "../globals.css";
import { useEffect } from "react";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";

export default function RootLayout({ children }) {
  // Initialize Bootstrap JS for transitions/toggles
  useEffect(() => {
    import("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <Navbar />
        <Sidebar />
        <main className="container-fluid py-4">
          {children}
        </main>
      </body>
    </html>
  );
}