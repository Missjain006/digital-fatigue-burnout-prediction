from app.db_connection import get_connection
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Load data from SQLite
conn = get_connection()
df = pd.read_sql("SELECT * FROM user_behavior", conn)
conn.close()

# 2. Select features
features = df[['screen_time', 'app_switches', 'late_night',
               'typing_speed', 'breaks']]

# 3. Normalize data (0–1)
scaler = MinMaxScaler()
scaled = scaler.fit_transform(features)
scaled_df = pd.DataFrame(scaled, columns=features.columns)

# 4. Inverse features
scaled_df['typing_speed'] = 1 - scaled_df['typing_speed']
scaled_df['breaks'] = 1 - scaled_df['breaks']

# 5. Calculate fatigue score
df['fatigue_score'] = (
    0.3 * scaled_df['screen_time'] +
    0.2 * scaled_df['app_switches'] +
    0.2 * scaled_df['late_night'] +
    0.15 * scaled_df['typing_speed'] +
    0.15 * scaled_df['breaks']
) * 100

# 6. Fatigue level
def fatigue_level(score):
    if score < 35:
        return "Low"
    elif score < 65:
        return "Medium"
    else:
        return "High"

df['fatigue_level'] = df['fatigue_score'].apply(fatigue_level)

# 7. Show result
print(df[['user_id', 'fatigue_score', 'fatigue_level']])
