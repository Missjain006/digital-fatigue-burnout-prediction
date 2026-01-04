from app.db_connection import get_connection
import pandas as pd

conn = get_connection()
df = pd.read_sql("SELECT * FROM user_behavior", conn)
conn.close()

print(df)
