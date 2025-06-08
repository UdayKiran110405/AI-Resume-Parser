// frontend/src/RawTextTab.js
import React, { useState, useEffect } from "react";

const RawTextTab = () => {
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/resumes");
      const data = await response.json();
      setResumes(data.resumes);
    } catch (error) {
      console.error("Error fetching resumes:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (resumeId) => {
    if (window.confirm("Are you sure you want to delete this resume?")) {
      try {
        await fetch(`http://localhost:8000/resume/${resumeId}`, {
          method: "DELETE",
        });
        fetchResumes(); // Refresh the list
      } catch (error) {
        console.error("Error deleting resume:", error);
      }
    }
  };

  const handleViewText = async (resumeId) => {
    try {
      const response = await fetch(`http://localhost:8000/resume/${resumeId}`);
      const resume = await response.json();
      setSelectedResume(resume);
    } catch (error) {
      console.error("Error fetching resume:", error);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="raw-text-tab">
      <h2>Extracted Text</h2>

      <div className="resume-list">
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>Name</th>
              <th>Upload Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {resumes.map((resume) => (
              <tr key={resume.id}>
                <td>{resume.filename}</td>
                <td>{resume.name || "N/A"}</td>
                <td>{new Date(resume.upload_date).toLocaleDateString()}</td>
                <td>
                  <button
                    className="action-button view"
                    onClick={() => handleViewText(resume.id)}
                  >
                    View Text
                  </button>
                  <button
                    className="action-button delete"
                    onClick={() => handleDelete(resume.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedResume && (
        <div className="text-display">
          <h3>Extracted Text from: {selectedResume.filename}</h3>
          <div className="text-content">
            {(selectedResume.raw_text || "").split("\n").map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
          </div>
          <button
            className="close-button"
            onClick={() => setSelectedResume(null)}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
};

export default RawTextTab;
