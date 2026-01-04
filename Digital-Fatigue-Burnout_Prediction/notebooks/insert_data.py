from app.db_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

data = [
    ('U1', 6.5, 40, 1, 38, 3, 3),
    ('U2', 9.0, 70, 1, 30, 1, 2),
    ('U3', 4.2, 20, 0, 45, 5, 4),
    ('U4', 7.8, 55, 1, 35, 2, 3),
    ('U5', 5.0, 25, 0, 42, 4, 4)
]

cursor.executemany("""
INSERT INTO user_behavior
(user_id, screen_time, app_switches, late_night, typing_speed, breaks, mood)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", data)

conn.commit()
conn.close()

print("Data inserted successfully")
