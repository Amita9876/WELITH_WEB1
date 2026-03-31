from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, HealthData, Achievement, AIChatHistory, Subscription
from datetime import datetime
from flask_migrate import Migrate
from openai import OpenAI
from models import Course
from models import Purchase

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

# ==============================
# DATABASE CONFIG
# ==============================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# ==============================
# HOME
# ==============================

@app.route("/")
def home():
    return render_template("home.html")


# ==============================
# SIGNUP
# ==============================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form.get("email")
        password = request.form["password"]

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("signup"))

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Create Free Subscription automatically
        free_plan = Subscription(
            plan_name="Free",
            price=0.0,
            user_id=new_user.id
        )
        db.session.add(free_plan)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for("login"))

    return render_template("signup.html")


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.")

    return render_template("login.html")


# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ==============================
# DASHBOARD
# ==============================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    records = HealthData.query.filter_by(
        user_id=session["user_id"]
    ).order_by(HealthData.date).all()

    achievements = Achievement.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "dashboard.html",
        records=records,
        achievements=achievements
    )

# ==============================
# REPORTS
# ==============================

@app.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect(url_for("login"))

    records = HealthData.query.filter_by(user_id=session["user_id"]).all()

    return render_template("reports.html", records=records)


# ==============================
# AI CHATBOT
# ==============================

client = OpenAI(api_key="YOUR_API_KEY")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "user_id" not in session:
        return redirect(url_for("login"))

    response = None

    if request.method == "POST":
        message = request.form["message"]

        ai = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a health and fitness AI coach."},
                {"role": "user", "content": message}
            ]
        )

        response = ai.choices[0].message.content

        chat_entry = AIChatHistory(
            user_message=message,
            ai_response=response,
            user_id=session["user_id"]
        )

        db.session.add(chat_entry)
        db.session.commit()

    chats = AIChatHistory.query.filter_by(user_id=session["user_id"]).all()

    return render_template("chatbot.html", response=response, chats=chats)

# ==============================
# INITIALIZE DATABASE
# ==============================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# ==============================
# COURSES ROUTE
# ==============================
@app.route("/courses")
def courses():

    all_courses = Course.query.all()

    return render_template(
        "courses.html",
        courses=all_courses
    )

# ==============================
# COURSES PURCHASES ROUTE
# ==============================
@app.route("/buy-course/<int:course_id>")
def buy_course(course_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    purchase = Purchase(
        user_id=session["user_id"],
        course_id=course_id
    )

    db.session.add(purchase)
    db.session.commit()

    flash("Course purchased successfully!")

    return redirect(url_for("courses"))