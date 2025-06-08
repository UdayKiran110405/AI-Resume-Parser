import sqlite3
import json
from datetime import datetime
import os

# Using SQLite for simplicity - you can replace with PostgreSQL later
DB_NAME = "resumes.db"

def init_database():
    """Initialize the database and create tables"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            name TEXT,
            email TEXT,
            phone TEXT,
            core_skills TEXT,
            soft_skills TEXT,
            work_experience TEXT,
            education TEXT,
            resume_rating INTEGER,
            improvement_areas TEXT,
            upskill_suggestions TEXT,
            raw_text TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def create_resume_record(filename, file_path, extracted_data, raw_text):
    """Create a new resume record in the database"""
    init_database()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO resumes (
            filename, file_path, name, email, phone, core_skills, 
            soft_skills, work_experience, education, resume_rating, 
            improvement_areas, upskill_suggestions, raw_text
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        file_path,
        extracted_data.get('name', ''),
        extracted_data.get('email', ''),
        extracted_data.get('phone', ''),
        json.dumps(extracted_data.get('core_skills', [])),
        json.dumps(extracted_data.get('soft_skills', [])),
        json.dumps(extracted_data.get('work_experience', [])),
        json.dumps(extracted_data.get('education', [])),
        extracted_data.get('resume_rating', 0),
        extracted_data.get('improvement_areas', ''),
        extracted_data.get('upskill_suggestions', ''),
        raw_text
    ))
    
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return resume_id

def get_all_resumes():
    """Get all resumes from database"""
    init_database()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, filename, name, email, phone, resume_rating, upload_date
        FROM resumes
        ORDER BY upload_date DESC
    ''')
    
    resumes = []
    for row in cursor.fetchall():
        resumes.append({
            'id': row[0],
            'filename': row[1],
            'name': row[2] or 'N/A',
            'email': row[3] or 'N/A',
            'phone': row[4] or 'N/A',
            'resume_rating': row[5],
            'upload_date': row[6]
        })
    
    conn.close()
    return resumes


def get_resume_by_id(resume_id):
    """Get specific resume by ID"""
    init_database()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM resumes WHERE id = ?
    ''', (resume_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        'id': row[0],
        'filename': row[1],
        'name': row[3],
        'email': row[4],
        'phone': row[5],
        'core_skills': json.loads(row[6]) if row[6] else [],
        'soft_skills': json.loads(row[7]) if row[7] else [],
        'work_experience': json.loads(row[8]) if row[8] else [],
        'education': json.loads(row[9]) if row[9] else [],
        'resume_rating': row[10],
        'improvement_areas': row[11],
        'upskill_suggestions': row[12],
        'raw_text': row[13] if row[13] else "",  # ✅ ADDED THIS LINE
        'upload_date': row[14]
    }
def delete_resume(resume_id):
    """Delete a resume record from database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # First get file path to delete the file
    cursor.execute('SELECT file_path FROM resumes WHERE id = ?', (resume_id,))
    file_path = cursor.fetchone()[0]
    
    # Delete database record
    cursor.execute('DELETE FROM resumes WHERE id = ?', (resume_id,))
    conn.commit()
    conn.close()
    
    # Delete the file
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return True