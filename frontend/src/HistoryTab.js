import React, { useState, useEffect } from 'react';

const HistoryTab = () => {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedResume, setSelectedResume] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/resumes');
      const data = await response.json();
      setResumes(data.resumes);
    } catch (error) {
      console.error('Error fetching resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDetailsClick = async (resumeId) => {
    try {
      const response = await fetch(`http://localhost:8000/resume/${resumeId}`);
      const resume = await response.json();
      setSelectedResume(resume);
      setShowModal(true);
    } catch (error) {
      console.error('Error fetching resume details:', error);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedResume(null);
  };

  const renderModal = () => {
    if (!showModal || !selectedResume) return null;

    return (
      <div className="modal-overlay" onClick={closeModal}>
        <div className="modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="modal-header">
            <h2>Resume Details</h2>
            <button className="close-button" onClick={closeModal}>×</button>
          </div>
          
          <div className="modal-body">
            <div className="personal-info">
              <h3>Personal Information</h3>
              <p><strong>Name:</strong> {selectedResume.name}</p>
              <p><strong>Email:</strong> {selectedResume.email}</p>
              <p><strong>Phone:</strong> {selectedResume.phone}</p>
            </div>

            <div className="skills-section">
              <div className="core-skills">
                <h3>Core Skills</h3>
                <div className="skills-list">
                  {selectedResume.core_skills.map((skill, index) => (
                    <span key={index} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>

              <div className="soft-skills">
                <h3>Soft Skills</h3>
                <div className="skills-list">
                  {selectedResume.soft_skills.map((skill, index) => (
                    <span key={index} className="skill-tag soft">{skill}</span>
                  ))}
                </div>
              </div>
            </div>

            <div className="experience-section">
              <h3>Work Experience</h3>
              {selectedResume.work_experience.map((job, index) => (
                <div key={index} className="job-item">
                  <h4>{job.position} at {job.company}</h4>
                  <p className="duration">{job.duration}</p>
                  <p>{job.description}</p>
                </div>
              ))}
            </div>

            <div className="education-section">
              <h3>Education</h3>
              {selectedResume.education.map((edu, index) => (
                <div key={index} className="education-item">
                  <h4>{edu.degree}</h4>
                  <p>{edu.institution} - {edu.year}</p>
                </div>
              ))}
            </div>

            <div className="rating-section">
              <h3>Resume Rating</h3>
              <div className="rating">
                <span className="rating-score">{selectedResume.resume_rating}/10</span>
                <div className="rating-bar">
                  <div 
                    className="rating-fill" 
                    style={{width: `${selectedResume.resume_rating * 10}%`}}
                  ></div>
                </div>
              </div>
            </div>

            <div className="suggestions-section">
              <div className="improvement-areas">
                <h3>Areas for Improvement</h3>
                <p>{selectedResume.improvement_areas}</p>
              </div>

              <div className="upskill-suggestions">
                <h3>Upskilling Suggestions</h3>
                <p>{selectedResume.upskill_suggestions}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return <div className="loading">Loading resumes...</div>;
  }

  return (
    <div className="history-tab">
      <h2>Resume History</h2>
      
      {resumes.length === 0 ? (
        <div className="no-resumes">
          <p>No resumes uploaded yet. Upload your first resume in the Upload tab!</p>
        </div>
      ) : (
        <div className="resumes-table">
          <table>
            <thead>
              <tr>
                <th>File Name</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Rating</th>
                <th>Upload Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {resumes.map((resume) => (
                <tr key={resume.id}>
                  <td>{resume.filename}</td>
                  <td>{resume.name}</td>
                  <td>{resume.email}</td>
                  <td>{resume.phone}</td>
                  <td>
                    <span className="rating-badge">
                      {resume.resume_rating}/10
                    </span>
                  </td>
                  <td>{new Date(resume.upload_date).toLocaleDateString()}</td>
                  <td>
                    <button
                      className="details-button"
                      onClick={() => handleDetailsClick(resume.id)}
                    >
                      Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {renderModal()}
    </div>
  );
};

export default HistoryTab; 
