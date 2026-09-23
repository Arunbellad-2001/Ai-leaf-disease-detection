import os
import re
import json
import base64
from io import BytesIO
from typing import Dict, List, Optional
from datetime import datetime

# --- Gemini Imports ---
from google import genai
from google.genai.errors import APIError # Use the correct API Error class
# --- End Gemini Imports ---

# --- Third-Party Libraries ---
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Pydantic Data Model ---
class DiseaseAnalysisResult(BaseModel):
    """Schema for the final analysis result returned to the frontend."""
    disease_detected: bool = Field(False, description="True if a disease or pest is detected.")
    disease_name: Optional[str] = Field(None, description="The common name of the detected disease.")
    disease_type: str = Field('unknown', description="Category: fungal, bacterial, viral, pest, or healthy.")
    severity: str = Field('unknown', description="Severity assessment: low, medium, or high.")
    confidence: float = Field(0.0, description="AI model's confidence in the detection (0.0 to 100.0).")
    plant_species: str = Field('Unknown Plant', description="The common name of the leaf identified.")
    symptoms: List[str] = Field([], description="List of observed symptoms.")
    possible_causes: List[str] = Field([], description="List of possible causes.")
    treatment: List[str] = Field([], description="Actionable steps for treatment/prevention.")
    analysis_timestamp: str = Field(..., description="Timestamp of the analysis.")


# --- Core Detection Logic Class ---
class LeafDiseaseDetector:
    
    # Use Gemini model name
    MODEL_NAME = "gemini-2.5-flash" 
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_MAX_TOKENS = 4096

    def __init__(self):
        # Initialize Gemini API client
        try:
            # Assumes GEMINI_API_KEY is set in .env or environment
            self.client = genai.Client() 
            print("Gemini Client Initialized.")
        except Exception as e:
            # Handle initialization failure (e.g., missing API key)
            print(f"Error initializing Gemini client. Check GEMINI_API_KEY: {e}")
            self.client = None # Set client to None on failure

    def create_analysis_prompt(self) -> str:
        """Generates the detailed prompt for the AI model."""
        return """
        Analyze the uploaded plant leaf image. Your first and most critical task is to **identify the common name of the plant leaf** and use it for the 'plant_species' field. If you cannot identify the disease, still identify the leaf.

        Provide your complete analysis in the following JSON format ONLY.
        Your response MUST be a single, clean JSON object enclosed in curly braces {}. Do not include any text, markdown (like ```json), or explanation outside the JSON object.

        JSON structure:
        {
          "disease_detected": true/false,
          "disease_name": "Common name of the disease or 'Healthy Leaf' if none",
          "disease_type": "fungal/bacterial/viral/pest/healthy/invalid_image",
          "severity": "low/medium/high/healthy",
          "confidence": 0.0 to 100.0 (percentage),
          "plant_species": "Common name of the leaf (e.g., 'Tomato', 'Apple', 'Oak'). **DO NOT use 'Unknown Leaf' unless absolutely necessary.**",
          "symptoms": ["List of observed symptoms (max 3)"],
          "possible_causes": ["List of possible causes (max 3)"],
          "treatment": ["List of actionable treatment steps (max 3)"]
        }
        
        If the image is not a plant or a leaf, set "disease_type" to "invalid_image", "disease_detected" to false, and set "disease_name" to "Invalid Image Content".
        """

    def _parse_response(self, response_content: str) -> DiseaseAnalysisResult:
        """
        PARSE FIX: Aggressively extracts and cleans the JSON block from the AI's response.
        """
        try:
            # 1. Aggressively isolate the JSON block using regex.
            json_match = re.search(r'\{.*\}', response_content.strip(), re.DOTALL)
            
            if not json_match:
                print(f"ERROR: Could not find a JSON block. Raw response: {response_content[:300]}...")
                raise ValueError("AI response did not contain a recognizable JSON structure.")

            cleaned_response = json_match.group(0).strip()
            
            # 2. Clean up common markdown code fences
            cleaned_response = re.sub(r'```json\n|```|```\n', '', cleaned_response).strip()
            
            # 3. Parse JSON
            disease_data = json.loads(cleaned_response)

            # --- ROBUST PLANT SPECIES CHECK (Fixes "Unknown Plant") ---
            plant_species_raw = disease_data.get('plant_species')
            
            if isinstance(plant_species_raw, str):
                plant_species = plant_species_raw.strip()
                if not plant_species:
                    plant_species = 'Unknown or Unspecified Leaf'
            else:
                plant_species = 'Unknown or Unspecified Leaf'
            # --- END ROBUST LOGIC ---

            # 4. Create and return the result object
            return DiseaseAnalysisResult(
                disease_detected=bool(
                    disease_data.get('disease_detected', False)),
                disease_name=disease_data.get('disease_name', 'Healthy Leaf'),
                disease_type=disease_data.get('disease_type', 'healthy'),
                severity=disease_data.get('severity', 'healthy'),
                confidence=float(disease_data.get('confidence', 0)),
                plant_species=plant_species, # Use the cleaned/validated value
                symptoms=disease_data.get('symptoms', []),
                possible_causes=disease_data.get('possible_causes', []),
                treatment=disease_data.get('treatment', []),
                analysis_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Unable to parse final JSON. Check AI output for syntax errors. Error: {e}")
        except Exception as e:
            raise e

    def analyze_leaf_image_base64(self, base64_image: str,
                                 temperature: float = None,
                                 max_tokens: int = None) -> Dict:
        """
        CRASH FIX: Includes a check for a blank response immediately after the API call.
        """
        try:
            if not self.client:
                 raise HTTPException(status_code=500, detail="Gemini Client not initialized. Check your API Key.")
            
            if not isinstance(base64_image, str) or not base64_image:
                raise ValueError("base64_image must be a non-empty string")

            if base64_image.startswith('data:'):
                base64_image = base64_image.split(',', 1)[1]

            # Convert base64 to PIL Image
            image_bytes = base64.b64decode(base64_image)
            image_stream = BytesIO(image_bytes)
            # This converts bytes to an image object compatible with the Gemini SDK
            image_part = Image.open(image_stream) 

            # Prepare request parameters
            temperature = temperature or self.DEFAULT_TEMPERATURE
            max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
            analysis_prompt = self.create_analysis_prompt()

            # Make API request
            response = self.client.models.generate_content(
                model=self.MODEL_NAME,
                contents=[image_part, analysis_prompt],
                config={"temperature": temperature,
                        "max_output_tokens": max_tokens}
            )

            # --- CRITICAL BLANK RESPONSE CHECK (Prevents parsing crash) ---
            if not response.text or response.text.strip() == "":
                print("ERROR: Gemini returned an empty response text.")
                return {"error": "AI model returned an empty response. Check image quality or API status.",
                        "disease_type": "invalid_image", "plant_species": "Not a plant"}
            # --------------------------------------------------------------
            
            # Parse the response text
            result = self._parse_response(response.text)

            return result.model_dump() # Return as dictionary for JSON serialization

        except APIError as e:
            print(f"Gemini API Error: {str(e)}")
            return {"error": f"AI model API call failed: {str(e)}"}
        except Exception as e:
            # Catches ValueError from _parse_response and other exceptions
            print(f"Analysis failed: {str(e)}")
            return {"error": f"An unexpected error occurred during analysis: {str(e)}"}

# --- FastAPI Application Setup ---
app = FastAPI(title="Leaf Disease Detection Backend")
detector = LeafDiseaseDetector()

# --- Endpoint for Streamlit Frontend ---
@app.post("/disease-detection-file")
async def analyze_upload_file(file: UploadFile = File(...)):
    """
    Receives an image file, converts it to base64, and sends it to the AI for analysis.
    """
    try:
        # Read the file content
        image_bytes = await file.read()
        
        # Convert to base64 string
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # Analyze using the detector class
        analysis_result = detector.analyze_leaf_image_base64(base64_image)
        
        # If the result contains an 'error' key, return 500
        if "error" in analysis_result:
            # Raise an HTTPException so FastAPI formats the error correctly
            raise HTTPException(status_code=500, detail=analysis_result["error"])

        return analysis_result

    except HTTPException as h:
        raise h # Re-raise structured exceptions
    except Exception as e:
        print(f"File upload processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error during file processing: {e}")