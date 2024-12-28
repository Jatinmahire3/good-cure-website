import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a strong secret key

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

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")  # Page with options to choose Doctor or Patient

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

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ai_module")
def ai_module():
    return render_template("ai_module.html")

@app.route("/appointment_booking")
def appointment_booking():
    return render_template("appointment_booking.html")

@app.route("/doctor_profile")
def doctor_profile():
    return render_template("doctor_profile.html")

@app.route("/reviews_ratings")
def reviews_ratings():
    return render_template("reviews_ratings.html")

@app.route("/lab_results")
def lab_results():
    return render_template("lab_results.html")

@app.route("/virtual_waiting_room")
def virtual_waiting_room():
    return render_template("virtual_waiting_room.html")

# Create database tables if they don't exist
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables based on the models
    app.run(debug=True)
