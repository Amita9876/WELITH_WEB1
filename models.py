from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ==============================
# USER MODEL
# ==============================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=False)

    profile_image = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    health_records = db.relationship("HealthData", backref="user", lazy=True)
    achievements = db.relationship("Achievement", backref="user", lazy=True)
    chats = db.relationship("AIChatHistory", backref="user", lazy=True)
    subscriptions = db.relationship("Subscription", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"



# ==============================
# HEALTH DATA MODEL
# ==============================

class HealthData(db.Model):
    __tablename__ = "health_data"

    id = db.Column(db.Integer, primary_key=True)

    weight = db.Column(db.Float, nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=True)

    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<HealthData {self.weight}kg - {self.steps} steps>"


# ==============================
# ACHIEVEMENT MODEL
# ==============================

class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Achievement {self.title}>"


# ==============================
# AI CHAT HISTORY MODEL
# ==============================

class AIChatHistory(db.Model):
    __tablename__ = "ai_chat_history"

    id = db.Column(db.Integer, primary_key=True)

    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Chat {self.timestamp}>"


# ==============================
# SUBSCRIPTION MODEL (SaaS Ready)
# ==============================

class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)

    plan_name = db.Column(db.String(50), nullable=False)  # Free, Pro, Premium
    price = db.Column(db.Float, nullable=False)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    is_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Subscription {self.plan_name}>"
    

# ==============================
# COURSE SYSTEM
# ==============================

class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    duration = db.Column(db.String(50))

    level = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==============================
# COURSE PURCHASES
# ==============================
class Purchase(db.Model):

    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)