
"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from . import database

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    database.init_db()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Get all activities with their participants."""
    conn = database.get_db()
    cursor = conn.cursor()
    
    # Get all activities with their participants
    activities = {}
    cursor.execute('''
        SELECT a.*, GROUP_CONCAT(p.email) as participant_emails
        FROM activities a
        LEFT JOIN participants p ON a.name = p.activity_name
        GROUP BY a.name
    ''')
    
    for row in cursor.fetchall():
        activities[row['name']] = {
            'description': row['description'],
            'schedule': row['schedule'],
            'max_participants': row['max_participants'],
            'participants': row['participant_emails'].split(',') if row['participant_emails'] else []
        }
    
    conn.close()
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    conn = database.get_db()
    cursor = conn.cursor()

    # Validate activity exists
    cursor.execute('SELECT * FROM activities WHERE name = ?', (activity_name,))
    activity = cursor.fetchone()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Validate student is not already signed up
    cursor.execute('SELECT * FROM participants WHERE activity_name = ? AND email = ?',
                  (activity_name, email))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Already signed up for this activity")
    
    # Check if activity is full
    cursor.execute('SELECT COUNT(*) as count FROM participants WHERE activity_name = ?',
                  (activity_name,))
    current_participants = cursor.fetchone()['count']
    if current_participants >= activity['max_participants']:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add student
    cursor.execute('INSERT INTO participants (email, activity_name) VALUES (?, ?)',
                  (email, activity_name))
    conn.commit()
    conn.close()
    return {"message": f"Signed up {email} for {activity_name}"}


# Unregister endpoint moved here, after app and activities are defined
@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    conn = database.get_db()
    cursor = conn.cursor()

    # Validate activity exists
    cursor.execute('SELECT * FROM activities WHERE name = ?', (activity_name,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if student is registered
    cursor.execute('SELECT * FROM participants WHERE activity_name = ? AND email = ?',
                  (activity_name, email))
    if not cursor.fetchone():
        raise HTTPException(status_code=400, detail="Student not registered for this activity")

    # Remove student
    cursor.execute('DELETE FROM participants WHERE activity_name = ? AND email = ?',
                  (activity_name, email))
    conn.commit()
    conn.close()
    return {"message": f"Removed {email} from {activity_name}"}
