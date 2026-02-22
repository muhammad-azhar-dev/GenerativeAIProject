// app/layout.js
import "bootstrap/dist/css/bootstrap.min.css";
import "../globals.css";
import Navbar from "@/components/Navbar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
       <Navbar/>
        {children}
      </body>
    </html>
  );
}