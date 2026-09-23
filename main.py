import streamlit as st
import requests
import json # Ensure json is imported for potential error handling/debugging

# Set Streamlit theme to light and wide mode
st.set_page_config(
    page_title="Leaf Disease Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Enhanced modern CSS, updated for the green color theme (#4CAF50)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #f7f9fa 100%); /* Light green/off-white background */
    }
    .result-card {
        background: rgba(255,255,255,0.95);
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(44,62,80,0.10);
        padding: 2.5em 2em;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        transition: box-shadow 0.3s;
    }
    .result-card:hover {
        box-shadow: 0 8px 32px rgba(44,62,80,0.18);
    }
    .disease-title {
        color: #2e7d32; /* Darker green for disease title */
        font-size: 2.2em;
        font-weight: 700;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px #e0e0e0;
    }
    .species-title {
        color: #4CAF50; /* Primary green for species title */
        font-size: 1.5em;
        font-weight: 600;
        margin-top: 0.5em;
        margin-bottom: 1em;
        padding-bottom: 0.5em;
        border-bottom: 2px solid #e0e0e0;
    }
    .section-title {
        color: #2e7d32; /* Dark green for section titles */
        font-size: 1.25em;
        margin-top: 1.2em;
        margin-bottom: 0.5em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .timestamp {
        color: #616161;
        font-size: 0.95em;
        margin-top: 1.2em;
        text-align: right;
    }
    .info-badge {
        display: inline-block;
        background: #e8f5e9; /* Very light green background */
        color: #2e7d32; /* Dark green text */
        border-radius: 8px;
        padding: 0.3em 0.8em;
        font-size: 1em;
        margin-right: 0.5em;
        margin-bottom: 0.3em;
    }
    .stMetric > div:nth-child(1) {
        font-size: 1.1em; /* Adjust metric label font size */
        color: #2e7d32;
    }
    .symptom-list, .cause-list, .treatment-list {
        margin-left: 1em;
        margin-bottom: 0.5em;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center; margin-top: 1em;'>
        <span style='font-size:2.5em;'>🌿</span>
        <h1 style='color: #2e7d32; margin-bottom:0;'>AI-Based Leaf Disease Detection Systems</h1>
        <p style='color: #616161; font-size:1.15em;'>Upload a leaf image to detect diseases, identify the leaf, and get expert treatment recommendations.</p>
    </div>
""", unsafe_allow_html=True)

# WARNING: Ensure this API URL is accessible. It is likely the Vercel URL
# of your deployed FastAPI backend.
api_url = "http://127.0.0.1:8000"

# Initialize session state for result storage
if 'result' not in st.session_state:
    st.session_state.result = None

col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader(
        "Upload Leaf Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview")

with col2:
    if uploaded_file is not None:
        if st.button("🔍 Detect Disease & Identify leaf", use_container_width=True):
            st.session_state.result = None # Clear previous results
            with st.spinner("Analyzing image with Gemini Vision Model..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # NOTE: Ensure your FastAPI backend handles the /disease-detection-file endpoint
                    response = requests.post(
                        f"{api_url}/disease-detection-file", files=files)
                    
                    if response.status_code == 200:
                        st.session_state.result = response.json()
                    elif response.status_code == 422:
                        st.error("Validation Error: Please check the image file format.")
                        st.session_state.result = None
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.write("Server Response:", response.text)
                        st.session_state.result = None
                        
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not reach the backend API. Please check the `api_url`.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")

# --- Result Display Logic ---
if st.session_state.result is not None:
    result = st.session_state.result
    
    # Start the results card HTML container
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # 1. Handle API/Internal Errors
    if result.get("error"):
        st.markdown("<div class='disease-title' style='color: #d32f2f;'>❌ Error</div>", unsafe_allow_html=True)
        st.error(f"Analysis failed: {result['error']}")

    # 2. Handle Invalid Image (Non-leaf)
    elif result.get("disease_type") == "invalid_image":
        st.markdown("<div class='disease-title' style='color: #ff9800;'>⚠️ Invalid Image</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='species-title'>**Leaf Name:** {result.get('plant_species', 'N/A')}</div>", unsafe_allow_html=True)
        st.warning(
             "The AI determined this image does not contain a valid plant leaf. Please upload a clearer image of plant vegetation.")
        
    # 3. Handle Disease Detected
    elif result.get("disease_detected"):
        st.markdown(
            f"<div class='disease-title'>🦠 {result.get('disease_name', 'Disease Detected')}</div>", unsafe_allow_html=True)
        
        # --- NEW: Plant Species Display ---
        plant_species = result.get('plant_species', 'Unknown Plant')
        st.markdown(
            f"<div class='species-title'>🌿 **Leaf Name:** {plant_species}</div>", unsafe_allow_html=True)
        # ----------------------------------
        
        # Display key metrics using Streamlit Columns/Metrics
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric(label="Severity", value=result.get('severity', 'N/A'))
        with colB:
            st.metric(label="Type", value=result.get('disease_type', 'N/A'))
        with colC:
            confidence = float(result.get('confidence', 0))
            st.metric(label="Confidence", value=f"{confidence:.0f}%")
            
        st.markdown("<hr style='margin-top: 1em; margin-bottom: 1em;'>", unsafe_allow_html=True)


        # Symptoms
        st.markdown("<div class='section-title'>Symptoms</div>", unsafe_allow_html=True)
        st.markdown("<ul class='symptom-list'>", unsafe_allow_html=True)
        for symptom in result.get("symptoms", []):
            st.markdown(f"<li>{symptom}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        # Possible Causes
        st.markdown("<div class='section-title'>Possible Causes</div>", unsafe_allow_html=True)
        st.markdown("<ul class='cause-list'>", unsafe_allow_html=True)
        for cause in result.get("possible_causes", []):
            st.markdown(f"<li>{cause}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        # Treatment
        st.markdown("<div class='section-title'>Treatment</div>", unsafe_allow_html=True)
        st.markdown("<ul class='treatment-list'>", unsafe_allow_html=True)
        for treat in result.get("treatment", []):
            st.markdown(f"<li>{treat}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        
        st.markdown(
            f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>", unsafe_allow_html=True)
            
    # 4. Handle Healthy Leaf
    else:
        # Healthy leaf case
        st.markdown("<div class='disease-title' style='color: #4CAF50;'>✅ Healthy Leaf</div>", unsafe_allow_html=True)
        
        # --- NEW: Plant Species Display ---
        plant_species = result.get('plant_species', 'Unknown Plant')
        st.markdown(
            f"<div class='species-title'>🌿 **Leaf Name:** {plant_species}</div>", unsafe_allow_html=True)
        # ----------------------------------
        
        st.markdown(
            "<div style='color: #4caf50; font-size: 1.1em; margin-bottom: 1em;'>No disease detected in this leaf. The plant appears to be healthy!</div>", unsafe_allow_html=True)
        
        st.markdown(f"<span class='info-badge'>Confidence: {float(result.get('confidence', 0)):.0f}%</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='info-badge'>Status: {result.get('disease_type', 'healthy')}</span>", unsafe_allow_html=True)
        
        st.markdown(
            f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# --- End of Result Display Logic ---