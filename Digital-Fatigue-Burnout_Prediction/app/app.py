from flask import Flask, render_template, request
import numpy as np
import joblib
import os

# ---------------- FLASK CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ---------------- LOAD MODEL ----------------
model = joblib.load(os.path.join(BASE_DIR, "models", "burnout_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    fatigue_score = None
    fatigue_level = None
    burnout_result = None
    fatigue_message = None
    recommendations = []

    if request.method == "POST":
        # -------- USER INPUT --------
        screen_time = float(request.form["screen_time"])
        app_switches = int(request.form["app_switches"])
        late_night = int(request.form["late_night"])
        typing_speed = int(request.form["typing_speed"])
        breaks = int(request.form["breaks"])

        # -------- PREPARE DATA --------
        X = np.array([[screen_time, app_switches, late_night,
                       typing_speed, breaks]])
        X_scaled = scaler.transform(X)

        # -------- FATIGUE SCORE --------
        fatigue_score = (
            0.3 * X_scaled[0][0] +
            0.2 * X_scaled[0][1] +
            0.2 * X_scaled[0][2] +
            0.15 * (1 - X_scaled[0][3]) +
            0.15 * (1 - X_scaled[0][4])
        ) * 100

        # -------- FATIGUE LEVEL --------
        if fatigue_score < 35:
            fatigue_level = "Low"
            fatigue_message = "🟢 You are digitally healthy. Keep maintaining good habits."
        elif fatigue_score < 65:
            fatigue_level = "Medium"
            fatigue_message = "🟠 You are experiencing digital tiredness. Small changes can help."
        else:
            fatigue_level = "High"
            fatigue_message = "🔴 You are digitally exhausted. Immediate attention is recommended."

        # -------- BURNOUT PREDICTION --------
        burnout = model.predict(X_scaled)[0]
        burnout_result = "High Risk" if burnout == 1 else "Low Risk"

        # -------- RECOMMENDATIONS --------
        if screen_time > 8:
            recommendations.append("Reduce daily screen time by at least 1–2 hours.")
        if late_night == 1:
            recommendations.append("Avoid screen usage after 11 PM.")
        if app_switches > 50:
            recommendations.append("Reduce frequent app switching to improve focus.")
        if breaks <= 2:
            recommendations.append("Take a 5-minute break after every 40 minutes of work.")
        if fatigue_level == "High":
            recommendations.append("Plan a digital detox or offline activities on weekends.")

    return render_template(
        "index.html",
        fatigue_score=fatigue_score,
        fatigue_level=fatigue_level,
        burnout_result=burnout_result,
        fatigue_message=fatigue_message,
        recommendations=recommendations
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


