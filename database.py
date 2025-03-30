import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect("fitness_tracker.db")
cursor = conn.cursor()

# Create a table to store user details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        height REAL NOT NULL,
        weight REAL NOT NULL,
        gender TEXT NOT NULL
    )
''')

# Create a table to store fitness records
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fitness_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        steps INTEGER NOT NULL,
        calories_burned REAL NOT NULL,
        heart_rate INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()
print("Database setup complete!")
