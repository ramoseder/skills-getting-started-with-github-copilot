"""Database operations for the High School Activities application."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "activities.db"

def get_db():
    """Create a database connection and return the connection and cursor."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    """Initialize the database with tables."""
    conn = get_db()
    cursor = conn.cursor()

    # Create activities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        name TEXT PRIMARY KEY,
        description TEXT NOT NULL,
        schedule TEXT NOT NULL,
        max_participants INTEGER NOT NULL
    )
    ''')

    # Create participants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        email TEXT NOT NULL,
        activity_name TEXT NOT NULL,
        FOREIGN KEY (activity_name) REFERENCES activities (name),
        PRIMARY KEY (email, activity_name)
    )
    ''')

    # Insert initial activities data
    initial_activities = [
        ("Chess Club", "Learn strategies and compete in chess tournaments", "Fridays, 3:30 PM - 5:00 PM", 12),
        ("Programming Class", "Learn programming fundamentals and build software projects", "Tuesdays and Thursdays, 3:30 PM - 4:30 PM", 20),
        ("Gym Class", "Physical education and sports activities", "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", 30),
        ("Soccer Team", "Join the school soccer team and compete in local leagues", "Tuesdays and Thursdays, 4:00 PM - 5:30 PM", 18),
        ("Basketball Club", "Practice basketball skills and play friendly matches", "Wednesdays, 3:30 PM - 5:00 PM", 15),
        ("Drama Club", "Participate in school plays and acting workshops", "Mondays, 4:00 PM - 5:30 PM", 20),
        ("Art Workshop", "Explore painting, drawing, and sculpture techniques", "Thursdays, 3:30 PM - 5:00 PM", 16),
        ("Math Olympiad", "Prepare for math competitions and solve challenging problems", "Fridays, 2:00 PM - 3:30 PM", 10),
        ("Science Club", "Conduct experiments and explore scientific concepts", "Wednesdays, 4:00 PM - 5:00 PM", 14)
    ]

    cursor.executemany('''
    INSERT OR REPLACE INTO activities (name, description, schedule, max_participants)
    VALUES (?, ?, ?, ?)
    ''', initial_activities)

    # Insert initial participants
    initial_participants = [
        ("michael@mergington.edu", "Chess Club"),
        ("daniel@mergington.edu", "Chess Club"),
        ("emma@mergington.edu", "Programming Class"),
        ("sophia@mergington.edu", "Programming Class"),
        ("john@mergington.edu", "Gym Class"),
        ("olivia@mergington.edu", "Gym Class"),
        ("lucas@mergington.edu", "Soccer Team"),
        ("mia@mergington.edu", "Soccer Team"),
        ("liam@mergington.edu", "Basketball Club"),
        ("ava@mergington.edu", "Basketball Club"),
        ("noah@mergington.edu", "Drama Club"),
        ("isabella@mergington.edu", "Drama Club"),
        ("amelia@mergington.edu", "Art Workshop"),
        ("benjamin@mergington.edu", "Art Workshop"),
        ("charlotte@mergington.edu", "Math Olympiad"),
        ("jackson@mergington.edu", "Math Olympiad"),
        ("harper@mergington.edu", "Science Club"),
        ("logan@mergington.edu", "Science Club")
    ]

    cursor.executemany('''
    INSERT OR REPLACE INTO participants (email, activity_name)
    VALUES (?, ?)
    ''', initial_participants)

    conn.commit()
    conn.close()
