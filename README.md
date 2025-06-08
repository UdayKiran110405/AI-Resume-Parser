# AI Resume Parser

An AI-powered resume parser that extracts information from PDF resumes and provides intelligent analysis and upskilling suggestions using Google's Gemini API.

## Features

- **Upload & Analyze**: Upload PDF resumes and get AI-powered analysis
- **Information Extraction**: Extracts personal info, skills, experience, education
- **Resume Rating**: Get a rating out of 10 for your resume
- **Improvement Suggestions**: AI-generated suggestions for resume improvement
- **Upskilling Recommendations**: Personalized skill development suggestions
- **History Tracking**: View all previously uploaded resumes in a table
- **Detailed View**: Click to see full analysis of any past resume

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Database**: SQLite (easily replaceable with PostgreSQL)
- **AI**: Google Gemini API
- **PDF Processing**: PyPDF2

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install dependencies:

```bash
pip install -r ../requirements.txt
```

3. Set up your Gemini API key:

   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set environment variable: `export GEMINI_API_KEY=your_api_key_here`
   - Or edit the API key directly in `main.py`

4. Run the backend server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install react react-dom react-scripts
```

3. Start the development server:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Upload Resume**: Go to the "Upload Resume" tab, select a PDF file, and click "Upload & Analyze"
2. **View Analysis**: See extracted information, skills, rating, and AI suggestions
3. **Check History**: Go to "Resume History" tab to see all uploaded resumes
4. **View Details**: Click "Details" button on any resume to see full analysis

## API Endpoints

- `POST /upload-resume` - Upload and analyze a resume
- `GET /resumes` - Get all uploaded resumes
- `GET /resume/{id}` - Get specific resume details
- `GET /health` - Health check

## Sample Data

Place sample PDF resumes in the `sample_data/` folder for testing.

## Screenshots

Add screenshots of your application in the `screenshots/` folder:

- Upload page
- Analysis results
- History table
- Details modal

## Future Enhancements

- PostgreSQL integration
- User authentication
- Resume comparison
- Export functionality
- Advanced analytics dashboard
