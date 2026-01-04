from app.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_behavior (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    screen_time REAL,
    app_switches INTEGER,
    late_night INTEGER,
    typing_speed INTEGER,
    breaks INTEGER,
    mood INTEGER
)
""")

conn.commit()
conn.close()

print("Table created successfully")
