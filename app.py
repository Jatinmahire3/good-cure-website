import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong secret key

# Set up database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "instance", "app.db")

# Ensure the 'instance' directory exists
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False)  # 'Doctor' or 'Patient'
    name = db.Column(db.String(100), nullable=False)
    age_or_speciality = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")  # Main signup page with links to doctor/patient signup

@app.route("/signup/doctor", methods=["GET", "POST"])
def signup_doctor():
    if request.method == "POST":
        name = request.form["name"]
        speciality = request.form["speciality"]
        password = request.form["password"]

        # Save to database
        new_user = User(role="Doctor", name=name, age_or_speciality=speciality, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Doctor account created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("signup_doctor.html")

@app.route("/signup/patient", methods=["GET", "POST"])
def signup_patient():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        password = request.form["password"]

        # Save to database
        new_user = User(role="Patient", name=name, age_or_speciality=age, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Patient account created successfully!", "success")
        return redirect(url_for("home"))

    return render_template("signup_patient.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # Query user from database
        user = User.query.filter_by(name=name, password=password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
