import sqlite3

def register_user(name, age, height, weight, gender):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, age, height, weight, gender) VALUES (?, ?, ?, ?, ?)",
                   (name, age, height, weight, gender))

    conn.commit()
    conn.close()
    print("User registered successfully!")

# check if a user exists
def check_user(name):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()

    conn.close()
    return user  

def log_fitness_data(user_name, date, steps, calories_burned, heart_rate):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE name = ?", (user_name,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("INSERT INTO fitness_data (user_id, date, steps, calories_burned, heart_rate) VALUES (?, ?, ?, ?, ?)",
                       (user_id, date, steps, calories_burned, heart_rate))
        conn.commit()
        conn.close()
        return True  
    else:
        conn.close()
        return False 

def get_fitness_data(user_name):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fitness_data.date, fitness_data.steps, fitness_data.calories_burned, fitness_data.heart_rate
        FROM fitness_data
        JOIN users ON fitness_data.user_id = users.id
        WHERE users.name = ?
        ORDER BY fitness_data.date DESC
    """, (user_name,))

    records = cursor.fetchall()
    conn.close()
    return records  
