//frontend/src/uploadTab.js
import React, { useState } from "react";

const UploadTab = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a PDF file");
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload-resume", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // Attempt to read error message from response body
        let errorMessage = "Upload failed";
        try {
          const errorBody = await response.json();
          if (errorBody.detail) {
            errorMessage = errorBody.detail;
          } else if (errorBody.error_message) {
            // Check for backend fallback message
            errorMessage = errorBody.error_message;
          }
        } catch (jsonError) {
          console.error("Failed to parse error response:", jsonError);
        }
        throw new Error(errorMessage);
      }

      const result = await response.json();
      setAnalysis(result);
      // Optionally clear file selection after successful upload
      // setFile(null);
    } catch (err) {
      setError("Error uploading file: " + err.message);
      setAnalysis(null); // Clear previous analysis on error
    } finally {
      setLoading(false);
    }
  };

  const renderAnalysis = () => {
    if (!analysis) return null;

    // Helper function to check if a property exists and is an array
    const isArrayAndNotEmpty = (data, prop) => {
      return data && Array.isArray(data[prop]) && data[prop].length > 0;
    };

    return (
      <div className="analysis-results">
        <h2>Resume Analysis Results</h2>

        <div className="personal-info">
          <h3>Personal Information</h3>
          <p>
            <strong>Name:</strong> {analysis.name || "N/A"}
          </p>
          <p>
            <strong>Email:</strong> {analysis.email || "N/A"}
          </p>
          <p>
            <strong>Phone:</strong> {analysis.phone || "N/A"}
          </p>
        </div>

        <div className="skills-section">
          <div className="core-skills">
            <h3>Core Skills</h3>
            <div className="skills-list">
              {isArrayAndNotEmpty(analysis, "core_skills") ? (
                analysis.core_skills.map((skill, index) => (
                  <span key={index} className="skill-tag">
                    {skill}
                  </span>
                ))
              ) : (
                <p>No core skills found.</p>
              )}
            </div>
          </div>
          <div className="soft-skills">
            <h3>Soft Skills</h3>
            <div className="skills-list">
              {isArrayAndNotEmpty(analysis, "soft_skills") ? (
                analysis.soft_skills.map((skill, index) => (
                  <span key={index} className="skill-tag soft">
                    {skill}
                  </span>
                ))
              ) : (
                <p>No soft skills found.</p>
              )}
            </div>
          </div>
        </div>

        <div className="experience-section">
          <h3>Work Experience</h3>
          {isArrayAndNotEmpty(analysis, "work_experience") ? (
            analysis.work_experience.map((job, index) => (
              <div key={index} className="job-item">
                <h4>
                  {job.position || "N/A"} at {job.company || "N/A"}
                </h4>
                <p className="duration">{job.duration || "N/A"}</p>
                <p>{job.description || "No description available."}</p>
              </div>
            ))
          ) : (
            <p>No work experience found.</p>
          )}
        </div>

        <div className="education-section">
          <h3>Education</h3>
          {isArrayAndNotEmpty(analysis, "education") ? (
            analysis.education.map((edu, index) => (
              <div key={index} className="education-item">
                <h4>{edu.degree || "N/A"}</h4>
                <p>
                  {edu.institution || "N/A"} - {edu.year || "N/A"}
                </p>
              </div>
            ))
          ) : (
            <p>No education information found.</p>
          )}
        </div>

        <div className="rating-section">
          <h3>Resume Rating</h3>
          <div className="rating">
            {analysis.resume_rating !== undefined &&
            analysis.resume_rating !== null ? (
              <>
                <span className="rating-score">
                  {analysis.resume_rating}/10
                </span>
                <div className="rating-bar">
                  <div
                    className="rating-fill"
                    style={{ width: `${analysis.resume_rating * 10}%` }}
                  ></div>
                </div>
              </>
            ) : (
              <p>Rating not available.</p>
            )}
          </div>
        </div>

        <div className="suggestions-section">
          <div className="improvement-areas">
            <h3>Areas for Improvement</h3>
            <p>
              {analysis.improvement_areas ||
                "No specific areas for improvement provided."}
            </p>
          </div>
          <div className="upskill-suggestions">
            <h3>Upskilling Suggestions</h3>
            <p>
              {analysis.upskill_suggestions ||
                "No upskilling suggestions provided."}
            </p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="upload-tab">
      <div className="upload-section">
        <h2>Upload Your Resume</h2>
        <div className="file-upload">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="file-input"
            id="resumeFile" // Added ID for better accessibility
          />
          <label htmlFor="resumeFile" className="file-input-label">
            {" "}
            {/* Added label for better accessibility */}
            {file ? `Selected: ${file.name}` : "Choose a PDF file"}
          </label>
          {file && <p className="file-selected">Selected: {file.name}</p>}
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="upload-button"
          >
            {loading ? "Analyzing..." : "Upload & Analyze"}
          </button>
        </div>
        {error && (
          <div className="error-message" role="alert">
            {" "}
            {/* Added role for accessibility */}
            {error}
          </div>
        )}
        {analysis &&
          analysis.status === "error" && ( // Display backend error message if status is error
            <div className="error-message" role="alert">
              Backend Error: {analysis.error_message || "Analysis failed."}
            </div>
          )}
      </div>
      {renderAnalysis()}
    </div>
  );
};

export default UploadTab;
