import sqlite3

# --- TIMETABLE DATA (Consolidated and Cleaned) ---
# Each tuple is (Division, Day, Time, Subject, Location)
TIMETABLES_DATA = [
    # DIVISION A
    ("DIVISION A", "MONDAY", "1st Hour (9-10 AM)", "M-1", "Batch-everyone"),
    ("DIVISION A", "MONDAY", "2nd Hour (10-11 AM)", "PHY", "Batch-everyone"),
    ("DIVISION A", "MONDAY", "(11-11:15AM)", "Short Break", "Canteen"),
    ("DIVISION A", "MONDAY", "3rd Hour (11:15-1:15 AM)", "EM", "Batch A1"),
    ("DIVISION A", "MONDAY", "3rd Hour (11:15-1:15 AM)", "BEE", "Batch A2"),
    ("DIVISION A", "MONDAY", "3rd Hour and 4th Hour (11:15-1:15 AM)", "PHY", "Batch A3"),
    ("DIVISION A", "MONDAY", "1:15-2 PM", "Long Break", "Canteen/Home"),
    
    
    # DIVISION B
    ("DIVISION B", "MONDAY", "1st Hour (9-10 AM)", "EM", "Batch-everyone"),
    ("DIVISION B", "MONDAY", "2nd Hour (10-11 AM)", "FPL", "Batch-everyone"),
    ("DIVISION B", "MONDAY", "(11-11:15AM)", "Short Break", "Canteen"),
    ("DIVISION B", "MONDAY", "3rd Hour (11:15-12:15 AM)", "PHY", "Everyone"),
    ("DIVISION B", "MONDAY", "3rd Hour (12:15-1:15 AM)", "M1", "Everyone"),
    ("DIVISION B", "MONDAY", "1:15-2 PM", "Long Break", "Canteen/Home"),
   
]

def setup_database():
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    # 1. Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            division TEXT NOT NULL,
            day TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            subject TEXT NOT NULL,
            location TEXT
        )
    """)
    
    # 2. Clear existing data (optional, for safe re-runs)
    cursor.execute("DELETE FROM schedule")

    # 3. Insert the timetable data
    # Note: We skip the first column (id) since it's AUTOINCREMENT
    insert_query = """
        INSERT INTO schedule (division, day, time_slot, subject, location)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_query, TIMETABLES_DATA)

    # 4. Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database 'timetable.db' created and populated successfully.")

if __name__ == '__main__':
    setup_database()