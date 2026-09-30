from flask import Flask, render_template, request

app = Flask(__name__)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# STUDY PLANNER
# ==========================================

@app.route("/planner", methods=["GET", "POST"])
def planner():

    plan = None

    if request.method == "POST":

        subject = request.form.get("subject")
        hours = float(request.form.get("hours"))
        days = int(request.form.get("days"))

        plan = []

        for day in range(1, days + 1):

            session_time = round(hours / 2, 1)

            plan.append({
                "day": day,
                "session1": f"Study {subject} - Session 1 ({session_time} hours)",
                "session2": f"Study {subject} - Session 2 ({session_time} hours)"
            })

    return render_template("planner.html", plan=plan)


# ==========================================
# BURNOUT PREDICTOR
# ==========================================

def predict_burnout(study_hours, sleep_hours, breaks, stress_level, tasks):

    score = 0

    if study_hours > 8:
        score += 3
    elif study_hours > 6:
        score += 2
    elif study_hours > 4:
        score += 1

    if sleep_hours < 5:
        score += 3
    elif sleep_hours < 7:
        score += 2

    if breaks < 2:
        score += 2
    elif breaks < 4:
        score += 1

    if stress_level >= 8:
        score += 3
    elif stress_level >= 5:
        score += 2
    elif stress_level >= 3:
        score += 1

    if tasks > 8:
        score += 3
    elif tasks > 5:
        score += 2
    elif tasks > 3:
        score += 1

    if score >= 9:
        return "High"
    elif score >= 5:
        return "Medium"
    else:
        return "Low"


@app.route("/burnout", methods=["GET", "POST"])
def burnout():

    result = None

    if request.method == "POST":

        study_hours = float(request.form.get("study_hours"))
        sleep_hours = float(request.form.get("sleep_hours"))
        breaks = int(request.form.get("breaks"))
        stress_level = int(request.form.get("stress_level"))
        tasks = int(request.form.get("tasks"))

        result = predict_burnout(
            study_hours,
            sleep_hours,
            breaks,
            stress_level,
            tasks
        )

    return render_template(
        "burnout.html",
        result=result
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)