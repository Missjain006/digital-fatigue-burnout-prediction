from app.db_connection import get_connection
import pandas as pd

# Load data
conn = get_connection()
df = pd.read_sql("SELECT * FROM user_behavior", conn)
conn.close()

# Recalculate fatigue score (same logic as before)
from sklearn.preprocessing import MinMaxScaler

features = df[['screen_time', 'app_switches', 'late_night',
               'typing_speed', 'breaks']]

scaler = MinMaxScaler()
scaled = scaler.fit_transform(features)
scaled_df = pd.DataFrame(scaled, columns=features.columns)

scaled_df['typing_speed'] = 1 - scaled_df['typing_speed']
scaled_df['breaks'] = 1 - scaled_df['breaks']

df['fatigue_score'] = (
    0.3 * scaled_df['screen_time'] +
    0.2 * scaled_df['app_switches'] +
    0.2 * scaled_df['late_night'] +
    0.15 * scaled_df['typing_speed'] +
    0.15 * scaled_df['breaks']
) * 100

# Create burnout label
df['burnout_risk'] = df['fatigue_score'].apply(lambda x: 1 if x >= 60 else 0)

print(df[['user_id', 'fatigue_score', 'burnout_risk']])
