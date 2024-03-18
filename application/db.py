import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import csv


import click
from flask import current_app, g

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database path

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
"""
# Create the Class Location Model
class ClassLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(100), nullable=False)
    campus_location = db.Column(db.String(100), nullable=False)

# Create the Course Details Model    
class CourseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(100), nullable=False)
    meeting_days = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.String(100), nullable=False)
    end_time = db.Column(db.String(100), nullable=False)
    section_name = db.Column(db.String(100), unique=True, nullable=False)
    short_title = db.Column(db.String(100))
    min_credits = db.Column(db.Integer, nullable=False)
    max_credits = db.Column(db.Integer, nullable=False)
    prerequisites = db.Column(db.String(100), nullable=False)
    seat_capacity = db.Column(db.Integer, nullable=False)
    seats_available = db.Column(db.Integer, nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    coreq = db.Column(db.String(100), nullable=False)
    avail_status = db.Column(db.String(100), nullable=False)
"""
# Create all tables
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
"""
# Populates the CLASSLOCATION table with data from the csv file
def load_class_location():
    file = open('CouseOfferings24SP-CLASSLOCATION.csv', 'r')
    reader = csv.DictReader(file)
    for row in reader:
        class_location = ClassLocation(building_name=row['BLDG'], campus_location=row['Location'])
        db.session.add(class_location)
    db.session.commit()

# Populates the COURSEDETAILS table with data from the csv file
def load_course_details():
    file = open('CouseOfferings24SP-COURSEDETAILS.csv', 'r')
    reader = csv.DictReader(file)
    for row in reader:
        course_details = CourseDetails(
            room_number=row['ROOM'],
            meeting_days=row['DAYS'],
            start_time=row['Start Time'],
            end_time=row['End Time'],
            section_name=row['SectionName'],
            short_title=row['ShortTitle'],
            min_credits=int(row['Min Creds']),
            max_credits=int(row['Max Creds']),
            prerequisites=row['Prerequisites'],
            seat_capacity=int(row['Seat Capatcity']),
            seats_available=int(row['Seats Available']),
            faculty_name=row['Faculty Name'],
            coreq=row['Coreq'],
            avail_status=row['Avail Status']
        )
        db.session.add(course_details)
    db.session.commit()
"""
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Protected route
@app.route('/')
@login_required
def index():
    return 'Hello, {}'.format(current_user.username)

if __name__ == '__main__':
    app.run(debug=True)



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()