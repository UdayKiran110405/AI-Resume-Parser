# AI Resume Parser

The AI Resume Parser is a powerful web application that leverages artificial intelligence to analyze and extract key information from resumes. This tool helps recruiters, HR professionals, and job seekers quickly understand resume content, identify strengths, and receive improvement suggestions.

## Key Features

1. **Resume Upload & Analysis**
   - Upload PDF resumes for AI-powered analysis
   - View detailed parsing results (personal info, skills, work experience, education)

2. **Resume History**
   - Track all uploaded resumes with metadata
   - View historical analysis results and ratings

3. **Extracted Text View**
   - Access raw extracted text from any uploaded resume
   - Manage your resume library with delete functionality

4. **AI-Powered Insights**
   - Automatic resume rating (0-10 scale)
   - Personalized improvement suggestions
   - Upskilling recommendations


## Screenshots

1. **Main Interface**
   
   ![Upload Interface](/Screenshot%202025-06-08%20210821.png)

2. **File Selection**
   
   ![File Selection](/Screenshot%202025-06-08%20211315.png)

3. **Analysis Results**
    
   <img src="localhost_3000_%20(5).png" alt="Analysis Results" width="600">

4. **Resume History**
   
   <img src="localhost_3000_%20(4).png" alt="Resume History" width="600">

5. **Extracted Text**
    
   <img src="localhost_3000_%20(6).png" alt="Extracted Text" width="600">


## Installation

```bash
# Clone repository
git clone https://github.com/UdayKiran110405/AI-Resume-Parser.git

# Install dependencies
pip install -r requirements.txt
cd frontend
npm install

# Run application
python backend/main.py  # Backend
npm start               # Frontend (from frontend directory)
```
## Usage Guide

### Step 1: Upload Your Resume
- Click the "Choose File" button
- Select a PDF resume from your device
- Supported formats: PDF only (max size: 5MB)

### Step 2: Analyze Your Resume
- Click the "Upload & Analyze" button
- Wait for processing (typically takes 10-30 seconds)
- View real-time progress indicator during analysis

### Step 3: Review Analysis Results
The system will display comprehensive insights including:

#### Personal Information
- Name
- Contact details (email, phone)
- LinkedIn/GitHub profiles (if available)

#### Professional Summary
- Core competencies
- Career objectives

#### Skills Analysis
- Technical skills categorized by proficiency
- Programming languages
- Frameworks and tools

#### Work Experience
- Chronological work history
- Role descriptions
- Key achievements and responsibilities

#### Education Background
- Degrees and certifications
- Institutions and graduation dates
- Academic achievements

#### Resume Rating (0-10 scale)
- Overall quality assessment
- Breakdown by section scores

#### Improvement Suggestions
- Content recommendations
- Formatting tips
- Skill enhancement opportunities

### Additional Features
- **History View**: Access all previously analyzed resumes
- **Compare Resumes**: Side-by-side comparison of multiple resumes
- **Export Options**: Download analysis reports in PDF/JSON format

## Project Structure
```bash
AI-RESUME-PARSER/
├── backend/
│   ├── uploads/
│   ├── database.py
│   ├── main.py
│   └── resumes.db
├── frontend/
├── sample_data/
│   └── screenshots/  # Contains all demo images
├── README.md
└── requirements.txt
```
## 🎥 Video Demo

[![Watch Demo](https://img.icons8.com/color/480/youtube-play.png)](https://drive.google.com/file/d/1whd1rt7j2PSJzpxoYk_XjjEsTM8co2IQ/view?usp=sharing)
📁 [Click here to watch the video on Google Drive](https://drive.google.com/file/d/1whd1rt7j2PSJzpxoYk_XjjEsTM8co2IQ/view?usp=sharing)

