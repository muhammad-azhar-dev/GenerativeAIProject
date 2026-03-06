"use client";
import React from "react";

export default function page() {
  const token = localStorage.getItem('token');

  const handleSubscription = async (planName) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/create-checkout-session", {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}`  },
                body: JSON.stringify({ plan: planName }) // Sirf 'basic' ya 'premium' bhej rahe hain
      });

      const data = await response.json();
      
      if (data.url) {
          window.location.href = data.url;
      } else {
          alert("Something went wrong!");
      }
    } catch (error) {
      console.error("Error creating checkout session:", error);
    }
  };
  return (
    <>
      <div className="container">
        <div className="row gap-5 justify-content-center">
            <div className="card text-white bg-primary mb-3" style={{maxWidth: "18rem"}}>
                <div className="card-header">Subcription Plan</div>
                    <div className="card-body">
                    <h5 className="card-title">Basic Plan</h5>
                    <h2>$05.00/month</h2>
                    <div className="d-flex flex-column gap-2">
                    <button className="btn btn-dark text-white mt-3" onClick={()=>{handleSubscription('basic')}}>Subscribe</button>
                    </div>
                    </div>
            </div>
            <div className="card text-white bg-primary mb-3" style={{maxWidth: "18rem"}}>
                <div className="card-header">Subcription Plan</div>
                    <div className="card-body">
                    <h5 className="card-title">Premium Plan</h5>
                    <h2>$15.00/month</h2>
                    <div className="d-flex flex-column gap-2">
                    <button className="btn btn-dark text-white mt-3" onClick={()=>{handleSubscription('premium')}}>Subscribe</button>
                    </div>
                    </div>
            </div>
        </div>
      </div>
    </>
  );
}
