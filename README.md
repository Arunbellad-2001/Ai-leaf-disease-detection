# 🌿 AI-Powered Leaf Disease Detection System

An enterprise-grade AI-powered leaf disease detection system featuring a dual-interface architecture: a FastAPI backend service and an interactive Streamlit web application. Built using **Google's Gemini Vision Model** via the `google-genai` SDK, this system provides accurate disease identification, severity assessment, **plant species identification**, and actionable treatment recommendations for agricultural and horticultural applications.

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
git clone [YOUR_REPO_URL]
cd [YOUR_REPO_NAME]
```

### 2\. Create and Activate Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3\. Install Dependencies

Install all required libraries, including the Gemini SDK, FastAPI, and Streamlit.

```bash
pip install -r requirements.txt
# Required packages: google-genai, fastapi, uvicorn, streamlit, python-dotenv, requests, Pillow
```

### 4\. Configure API Key

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
uvicorn Leaf\ Disease.main:app --reload
# Server will run on http://127.0.0.1:8000
```

### 2\. Start the Streamlit Frontend

Open a **new terminal tab** (while the backend is running) and start the Streamlit application:

```bash
streamlit run app.py
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