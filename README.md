# 🌿 AI-Based Leaf Disease Detection System

An end-to-end, multi-component AI web application that detects plant leaf diseases, identifies plant species, and provides detailed symptoms, causes, and expert treatment recommendations.

---

### 🌐 Live Application Links

* **Frontend Web App (Streamlit):** [https://ai-leaf-disease-detection-vmng66ct7ccvmzezts7ddx.streamlit.app](https://ai-leaf-disease-detection-vmng66ct7ccvmzezts7ddx.streamlit.app)
* **Backend API Service (Vercel):** [https://ai-leaf-disease-detection-seven.vercel.app](https://ai-leaf-disease-detection-seven.vercel.app)

---

### 📋 Overview of Recent Updates

* **AI Model Migration:** Upgraded the image reasoning engine to active Google Gemini Flash models (`gemini-1.5-flash` / `gemini-2.5-flash`) to ensure higher throughput and reliability.
* **Serverless Decoupled Deployment:** Migrated the backend to a serverless FastAPI setup on Vercel (`vercel.json`) and hosted the Streamlit user interface on Streamlit Cloud.
* **Memory-Optimized Image Handling:** Updated `/disease-detection-file` to stream image bytes directly into memory via `UploadFile`, eliminating local disk write dependencies on serverless environments.

---

### 🚀 Running the Project Locally

Follow these steps to set up and run both the backend API and frontend UI on your local machine.

#### Prerequisites

* Python 3.9+ installed
* A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

#### 1. Clone the Repository
```bash
git clone [https://github.com/Arunbellad-2001/leaf-diseases-detect.git](https://github.com/Arunbellad-2001/leaf-diseases-detect.git)
cd leaf-diseases-detect

## 🎯 Key Features

### Core Capabilities

  * **🔍 Advanced Disease Detection**: Identifies 500+ plant diseases across multiple categories (fungal, bacterial, viral, pest).
  * **🌿 Species Identification**: Accurately identifies the plant species from the leaf image before analysis.
  * **⚡ Real-time Analysis**: Provides diagnosis, severity, and confidence metrics in seconds.
  * **💊 Actionable Treatment Plans**: Generates specific, detailed recommendations for treatment and prevention.
  * **Robust Architecture**: Utilizes a highly stable FastAPI backend for processing and a modern Streamlit frontend for the user interface.

## ⚙️ System Architecture

The application follows a decoupled, three-tier architecture ensuring scalability and maintainability.

1.  **Frontend (Streamlit)**:
      * Provides a simple, responsive interface for image upload and result visualization.
      * Handles user session state and displays analysis results with clean formatting.
2.  **Backend (FastAPI)**:
      * Manages the `/disease-detection-file` API endpoint.
      * Handles image file upload, conversion to base64, and robust error handling.
      * Acts as the secure gateway to the AI engine.
3.  **AI Engine (Gemini Vision Model)**:
      * Uses the **`gemini-2.5-flash`** model (or similar) via the `google-genai` SDK.
      * Processes the image and a specialized prompt to return structured JSON containing the diagnosis and recommendations.

## 🚀 Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

  * Python 3.10+
  * A valid **Gemini API Key** (Obtainable from Google AI Studio).

### 1\. Clone the Repository

```bash
git [clone https://github.com/Arunbellad-2001/leaf-diseases-detect.git](https://github.com/Arunbellad-2001/leaf-diseases-detect.git)
cd [cd leaf-diseases-detect]
```

### 2\. Create and Activate Environment

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

### 3\. Configure API Key

Create a file named **`.env`** in the root directory and add your Gemini API key:

```
# .env file
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

## ▶️ Running the Application

The system requires both the backend and frontend to be running simultaneously.

### 1\. Start the FastAPI Backend

Navigate to the directory containing your `Leaf Disease/main.py` file and start the server:

```bash
python -m uvicorn app:app --reload
# Server will run on http://127.0.0.1:8000
```

### 2\. Start the Streamlit Frontend

Open a **new terminal tab** (while the backend is running) and start the Streamlit application:

```bash
streamlit run main.py
# Frontend will run on http://127.0.0.1:8501 (or similar)
```

Open your browser to the Streamlit address, upload an image, and click **"Detect Disease & Identify leaf."**

## ☁️ Deployment

This application is designed for easy serverless deployment:

  * **FastAPI Backend**: Recommended for deployment on **Vercel** or **Render**. Ensure the **`GEMINI_API_KEY`** is set as an **Environment Variable** in the platform's settings.
  * **Streamlit Frontend**: Easily deployable to **Streamlit Cloud**.

## 🤝 Contribution

Contributions are welcome\! Feel free to open issues or submit pull requests to enhance the model's accuracy, add new features, or improve the interface.

-----

\<div align="center"\>

**🌱 Empowering Agriculture Through AI-Driven Plant Health Solutions 🌱**

\</div\>