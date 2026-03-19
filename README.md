# Gen AI Document Processor (Next.js + FastAPI + Gemini 3 Flash)

A full-stack application that allows users to upload images and PDFs to extract insights using the **Gemini 3 Flash** model. 

## 🚀 Features
* **Multi-format Support:** Handles `.jpg`, `.jpeg`, `.png`, and `.pdf` files.
* **AI Analysis:** Powered by Google Gemini 3 Flash for fast and accurate content processing.
* **Local Storage:** Files are stored in a dedicated local directory with metadata saved in **MySQL**.
* **Modern UI:** Responsive frontend built with **Next.js**.
* **High Performance:** Backend powered by **FastAPI** for asynchronous processing.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js (React) |
| **Backend** | FastAPI (Python) |
| **Model** | Google Gemini 3 Flash |
| **Database** | MySQL (XAMPP / phpMyAdmin) |
| **Styling** | Bootstrap |

---

## 📋 Prerequisites
Before running the project, ensure you have:
* **XAMPP** (for MySQL)
* **Python 3.10+**
* **Node.js & npm**
* **Gemini API Key** (from Google AI Studio)

---

## ⚙️ Setup & Installation

### 1. Database Setup
1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Go to `http://localhost/phpmyadmin`.
3. Create a database named `gen_ai_db`.
4. Create a table for storing file paths:
   ```sql
   CREATE TABLE uploads (
       id INT AUTO_INCREMENT PRIMARY KEY,
       filename VARCHAR(255) NOT NULL,
       file_path VARCHAR(255) NOT NULL,
       analysis_output TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
## 🔄 Application Workflow

To understand how the system handles your files, here is the step-by-step logic:

1.  **Upload:** User selects a `.jpg`, `.png`, or `.pdf` via the Next.js frontend.
2.  **Validation:** The backend (FastAPI) checks the file extension and size.
3.  **Storage:** * The physical file is saved to the `/backend/uploads` directory with a unique timestamp.
    * The **relative path** and filename are stored in the `uploads` table in **MySQL**.
4.  **AI Processing:** The file is sent to the **Gemini 3 Flash** API with a predefined prompt.
5.  **Result:** The AI's JSON/Text response is returned to the frontend and optionally updated in the database.

---
