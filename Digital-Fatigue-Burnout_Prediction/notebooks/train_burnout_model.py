from app.db_connection import get_connection
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load data
conn = get_connection()
df = pd.read_sql("SELECT * FROM user_behavior", conn)
conn.close()

# Feature engineering
features = df[['screen_time', 'app_switches', 'late_night',
               'typing_speed', 'breaks']]

scaler = MinMaxScaler()
X = scaler.fit_transform(features)

# Fatigue score -> burnout label
df['fatigue_score'] = (
    0.3 * X[:,0] + 0.2 * X[:,1] + 0.2 * X[:,2] +
    0.15 * (1 - X[:,3]) + 0.15 * (1 - X[:,4])
) * 100

y = df['fatigue_score'].apply(lambda x: 1 if x >= 60 else 0)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/burnout_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("Burnout prediction model saved")
