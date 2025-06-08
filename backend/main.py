
import sqlite3
import json
from datetime import datetime
import os
import PyPDF2
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import io

# Assuming the database functions are in a file named database.py
# If not, you might need to include them here or adjust the import
from database import create_resume_record, get_all_resumes, get_resume_by_id, delete_resume, DB_NAME # Assuming delete_resume and DB_NAME are also in database.py

app = FastAPI(title="AI Resume Parser")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY", "AIzaSyDwjlyUR_Md8jnXtVVX4gC0UFTWASMLwmQ"), # Replace with your actual API key or environment variable
    transport='rest'
)

def extract_text_from_pdf(file_content):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or "" # Handle pages with no text
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def analyze_resume_with_gemini(resume_text):
    """Analyze resume using Gemini API with enhanced error handling and a robust prompt"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        Analyze the following resume text and extract detailed information.
        Provide the output strictly in the specified JSON format.

        Resume Text:
        {resume_text}

        Required JSON structure:
        {{
            "name": "Full name (extract accurately, default to 'Not Extracted' if not found)",
            "email": "Email address (extract accurately, look for @ symbol, default to 'Not Extracted' if not found)",
            "phone": "Phone number (extract accurately, digits only, include country code if present, default to 'Not Extracted' if not found)",
            "core_skills": ["List of technical/hard skills (extract as a list, default to empty array [])"],
            "soft_skills": ["List of interpersonal/soft skills (extract as a list, default to empty array [])"],
            "work_experience": [
                {{
                    "company": "Company name (exact, default to 'Unknown' if not found)",
                    "position": "Job title (exact, default to 'Unknown' if not found)",
                    "duration": "Employment period (e.g., '2020-Present', 'Jan 2018 - Dec 2019', default to 'Not Specified')",
                    "description": "Key responsibilities/achievements (extract as a concise string, default to 'No description available')"
                }}
                // Include all work experiences found
            ],
            "education": [
                {{
                    "degree": "Degree name (e.g., B.Sc Computer Science, M.A. History, default to 'Not Specified')",
                    "institution": "School/University name (exact, default to 'Unknown Institution')",
                    "year": "Graduation year or expected year (default to 'Not Specified')"
                }}
                // Include all education entries found
            ],
            "resume_rating": "Rate the resume's overall quality (content, formatting, completeness) on a scale of 1 to 10. Provide an integer value. Default to 5 if evaluation is not possible.",
            "improvement_areas": "Provide specific, constructive feedback on areas where the resume could be improved. Default to 'Analysis failed or no specific areas for improvement identified.' if not applicable.",
            "upskill_suggestions": "Suggest relevant skills or technologies the candidate could learn to enhance their profile, based on their current skills and experience. Default to 'No specific upskilling suggestions provided.' if not applicable."
        }}

        Rules for Extraction:
        1.  Return ONLY the JSON object. Do not include any additional text, markdown formatting (like ```json), or explanations outside the JSON.
        2.  Ensure accuracy for contact details (name, email, phone).
        3.  For lists (core_skills, soft_skills, work_experience, education), return an empty array [] if no relevant information is found.
        4.  For work experience and education entries, if a specific sub-field (like company, position, degree, institution, year, duration, description) is not found for an entry, use the specified default string ("Unknown", "Not Specified", "No description available").
        5.  The resume_rating must be an integer between 1 and 10.
        6.  If any section is completely missing or cannot be parsed, return the default values specified in the JSON structure description.
        7.  Be concise in descriptions.
        """
        # Removed request_options as it is not supported
        response = model.generate_content(prompt)

        response_text = response.text.strip()

        # Attempt to find JSON within the response
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        result = json.loads(response_text)

        # Validate presence and types of required fields
        required_fields = [
            'name', 'email', 'phone',
            'core_skills', 'soft_skills', 'work_experience', 'education',
            'resume_rating', 'improvement_areas', 'upskill_suggestions',
        ]
        if not all(k in result for k in required_fields):
            print("Warning: Gemini response missing expected keys.")
            return get_fallback_response()

        for arr_key in ['core_skills', 'soft_skills', 'work_experience', 'education']:
            if not isinstance(result.get(arr_key), list):
                print(f"Warning: {arr_key} is not a list. Using fallback.")
                return get_fallback_response()

        # Ensure resume_rating is an int in 1-10
        try:
            result['resume_rating'] = int(result.get('resume_rating', 5))
        except Exception:
            result['resume_rating'] = 5
        result['resume_rating'] = max(1, min(result['resume_rating'], 10))

        return result
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        return get_fallback_response("Failed to parse AI response as JSON.")
    except Exception as e:
        print(f"Gemini API or processing Error: {str(e)}")
        return get_fallback_response(f"Analysis failed due to an internal error: {str(e)}")

def get_fallback_response(error_message="Could not analyze resume. Please check the format and try again."):
    """Comprehensive fallback response when analysis fails"""
    return {
        "name": "Not Extracted",
        "email": "Not Extracted",
        "phone": "Not Extracted",
        "core_skills": [],
        "soft_skills": [],
        "work_experience": [],
        "education": [],
        "resume_rating": 5,
        "improvement_areas": error_message,
        "upskill_suggestions": "Consider ensuring your resume is clearly formatted and the text is easily readable."
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze resume"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        file_content = await file.read()

        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        upload_path = os.path.join("uploads", file.filename)

        # Handle potential filename conflicts
        counter = 1
        while os.path.exists(upload_path):
            name, ext = os.path.splitext(file.filename)
            upload_path = os.path.join("uploads", f"{name}_{counter}{ext}")
            counter += 1

        with open(upload_path, "wb") as f:
            f.write(file_content)

        resume_text = extract_text_from_pdf(file_content)
        analysis = analyze_resume_with_gemini(resume_text)

        # If fallback response was returned by analyze_resume_with_gemini
        if analysis.get("improvement_areas", "").startswith("Could not analyze resume") or analysis.get("improvement_areas", "").startswith("Failed to parse AI response") or analysis.get("improvement_areas", "").startswith("Analysis failed due to an internal error"):
             # Still save the record with fallback data and raw text
            resume_id = create_resume_record(
                filename=file.filename,
                file_path=upload_path,
                extracted_data=analysis, # Use fallback data
                raw_text=resume_text
            )
            analysis.update({
                'id': resume_id,
                'filename': file.filename,
                'upload_date': datetime.now().isoformat(),
                'status': 'error',
                'error_message': analysis.get("improvement_areas", "Analysis failed.") # Use improvement areas as error message
            })
            return JSONResponse(content=analysis, status_code=500) # Return 500 status for analysis failures


        resume_id = create_resume_record(
            filename=file.filename,
            file_path=upload_path,
            extracted_data=analysis,
            raw_text=resume_text
        )

        analysis.update({
            'id': resume_id,
            'filename': file.filename,
            'upload_date': datetime.now().isoformat(),
            'status': 'success'
        })

        return JSONResponse(content=analysis)

    except HTTPException as e:
        # Delete the partially saved file if upload was the issue
        if 'upload_path' in locals() and os.path.exists(upload_path):
             os.remove(upload_path)
        raise e
    except Exception as e:
        # Delete the partially saved file in case of other errors after saving
        if 'upload_path' in locals() and os.path.exists(upload_path):
             os.remove(upload_path)
        error_response = get_fallback_response(f"Processing failed: {str(e)}")
        error_response.update({
            'status': 'error',
            'error_message': str(e)
        })
        return JSONResponse(content=error_response, status_code=500)


@app.get("/resumes")
async def get_resumes():
    """Get all uploaded resumes"""
    try:
        resumes = get_all_resumes()
        return {"resumes": resumes, "count": len(resumes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resume/{resume_id}")
async def get_resume(resume_id: int):
    """Get specific resume details"""
    try:
        resume = get_resume_by_id(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/resume/{resume_id}")
async def delete_resume_endpoint(resume_id: int):
    """Delete a resume record and its file"""
    try:
        success = delete_resume(resume_id)
        if success:
             return {"status": "success", "message": "Resume deleted successfully"}
        else:
             raise HTTPException(status_code=404, detail="Resume not found") # Should be handled by delete_resume internally, but good practice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Service health check"""
    db_exists = os.path.exists(DB_NAME)
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected" if db_exists else "not found",
        "database_path": os.path.abspath(DB_NAME) # Optional: show DB path
    }

@app.get("/check-gemini")
async def check_gemini():
    """Check Gemini API connectivity"""
    try:
        # List models is a simple way to check connectivity and authentication
        models = genai.list_models()
        # Check if 'gemini-1.0-pro' is available, or just that list_models worked
        if any(model.name == 'models/gemini-1.0-pro' for model in models):
             return {"status": "connected", "model": "gemini-1.0-pro", "message": "Successfully connected to Gemini API."}
        else:
             # This might happen if the API key is valid but the model isn't available for the project/region
             return {"status": "warning", "model": "gemini-1.0-pro", "message": "Gemini 1.0 Pro model not found or accessible."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini API connection failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") # Added log_level for better output

