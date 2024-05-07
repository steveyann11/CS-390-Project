from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import subprocess

app = Flask(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with your own secret key
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database path

#db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
#id = db.Column(db.Integer, primary_key=True)
 #   username = db.Column(db.String(100), unique=True, nullable=False)
  #  password = db.Column(db.String(100), nullable=False)

# Create the user table
#db.create_all()

#@login_manager.user_loader
#def load_user(user_id):
 #   return User.query.get(int(user_id))


# Example user class (replace with your own user model)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Example user database (replace with your own user database)
users = {'user_id': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Example login form
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id in users and password == users[user_id]['password']:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')

    return render_template('login.html')

# Function to fetch data from the database
def get_data_from_location():
    conn = sqlite3.connect('../base_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CLASSLOCATION')
    data = cursor.fetchall()
    conn.close()
    return data


# Function to fetch data from the database
def get_data_from_details():
    conn = sqlite3.connect('../base_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM COURSEDETAILS')
    data = cursor.fetchall()
    conn.close()
    return data

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Protected route
@app.route('/')
#@login_required
def index():
    return render_template('homepage.html')

# Connects calendar page to database for schedule generation
@app.route('/calendar', methods=['GET', 'POST'])
#@login_required
def calendar():
    if request.method == 'POST':
        result = run_randomscheduler()
        data = get_data_from_location()  # assuming you still need to load this data
#        data.update(get_data_from_details())  # assuming these functions return dictionaries
        return render_template('calendar.html', data=data, result=result)
    else:
        data = get_data_from_location()
#        data.update(get_data_from_details())
        return render_template('calendar.html', data=data)
    
def run_randomscheduler():
    """
    Runs the code that is stored in RandomScheduler.py
    """
    process = subprocess.run(['python', 'RandomScheduler.py'], capture_output=True, text=True)
    output = process.stdout
    error = process.stderr
    if process.returncode == 0:
        return f'Classes: {output}'
    else:
        return f'An error occurred: {error}'


@app.route('/scheduling')
#@login_required
def scheduling():
    data = get_data_from_location()
    data = get_data_from_details()
    return render_template ('scheduling.html', data=data)

@app.route('/courses')
#@login_required
def courses():
    data = get_data_from_details()
    return render_template ('courses.html', data=data)

@app.route('/preference_schedule_maker')
def preference_schedule_maker():
    return render_template('preference_schedule_maker.html')

@app.route('/preference_schedule', methods=['POST'])
def preference_schedule_display():
    if request.method == 'POST':
        selected_classes = preference_scheduler()
        return render_template('preference_schedule.html', selected_classes=selected_classes)
    else:
        return render_template('preference_schedule.html')
    
# Functions needed in order for time to be compared and displayed properly
def convert_time_to_minutes(time):
    """
    Convert Times to number of minutes as integers so they can be compared easier

    Input: Time in a string format
    Output: Integer representing the time as minutes
    """
    hour, minute = time.split(':')
    minute, period = minute.split(' ')
    hour = int(hour)
    minute = int(minute)
    if period == 'PM' and hour != 12:
        hour += 12
    time_to_minutes = hour * 60 + minute
    return time_to_minutes
def revert_times(time):
    """
    Convert Times back to string so they can be displayed in the normal format
    
    Input: Integer value representing the time as minutes
    Output: String representing time in the 'hour:minute period' format
    """
    hour = time // 60
    minute = time % 60
    if hour < 12:
        period = 'AM'
    elif hour >= 12:
        period = 'PM'
        if hour > 12:
            hour = hour - 12
    return f"{hour}:{minute:02} {period}"

# Function to generate a schedule pased off personal preferences
def preference_scheduler():
    conn = sqlite3.connect('../base_database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        # Get the personal preferences
        BeginTime = request.form['StartTime']
        BeginTime = convert_time_to_minutes(BeginTime)
        StopTime = request.form['EndTime']
        StopTime = convert_time_to_minutes(StopTime)
        days = request.form.getlist('Days')  # Use getlist to get multiple checkbox values
        location = request.form['Location']
        NumClasses = int(request.form['NumberOfClasses'])

        # Create a query that will be used to gather the appropriate classes based on the users preferences
        sql_query = f"""
        SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cd.Coreq, cl.CampusLocation
        FROM COURSEDETAILS cd
        JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
        WHERE cd.StartTime >= '{BeginTime}' AND cd.StartTime < '{StopTime}'
        """

        # Define if statements to select classes on specific days
        meeting_days = []
        if 'M' in days:
            meeting_days.append("cd.MeetingDays LIKE '%M%'")
        if 'T' in days:
            meeting_days.append("cd.MeetingDays LIKE '%T%'")
        if 'W' in days:
            meeting_days.append("cd.MeetingDays LIKE '%W%'")
        if 'TH' in days:
            meeting_days.append("cd.MeetingDays LIKE '%TH%'")
        if 'F' in days:
            meeting_days.append("cd.MeetingDays LIKE '%F%'")
        # Add to query
        if meeting_days:
            sql_query += " AND (" + " OR ".join(meeting_days) + ")"

        # Define if statements to select classes in a specific location
        if location == "In Person":
            sql_query += " AND cl.CampusLocation = 'MC'"
        elif location == "Online":
            sql_query += " AND cl.CampusLocation = 'OL'"
        
        # Add ORDER BY RANDOM() to the main query directly
        sql_query += " ORDER BY RANDOM()"

        # Execute query
        cursor.execute(sql_query)
        all_classes = cursor.fetchall()  # Fetch all classes from the database

        # Makes sure that the classes returned don't overlap and have the proper coreqs
        time_slots = []
        selected_classes = []
        for class_info in all_classes:  # Iterate over fetched classes
            SectionName, ShortTitle, StartTime, EndTime, MeetingDays, Coreq, CampusLocation = class_info
            overlap = any(start < EndTime and end > StartTime for start, end in time_slots)
            if not overlap:
                # Revert times back to normal format before adding to selected classes
                StartTime_normal = revert_times(StartTime)
                EndTime_normal = revert_times(EndTime)
                class_info_with_normal_time = (SectionName, ShortTitle, StartTime_normal, EndTime_normal, MeetingDays, Coreq, CampusLocation)
                selected_classes.append(class_info_with_normal_time)
                time_slots.append((StartTime, EndTime))
                # Check if the class has a corequisite
                if Coreq:
                    cursor.execute(f"""
                    SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cd.Coreq, cl.CampusLocation
                    FROM COURSEDETAILS cd
                    JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
                    WHERE cd.SectionName = ? AND cd.StartTime >= ? AND cd.EndTime <= ?
                    """, (Coreq, StartTime, EndTime))
                    coreq_info = cursor.fetchone()
                    if coreq_info:
                        coreq_StartTime, coreq_EndTime = coreq_info[2], coreq_info[3]
                        StartTime_coreq_normal = revert_times(coreq_StartTime)
                        EndTime_coreq_normal = revert_times(coreq_EndTime)
                        coreq_info_with_normal_time = (coreq_info[0], coreq_info[1], StartTime_coreq_normal, EndTime_coreq_normal, coreq_info[4], coreq_info[5], coreq_info[6])
                        selected_classes.append(coreq_info_with_normal_time)
                        time_slots.append((coreq_StartTime, coreq_EndTime))
            if len(selected_classes) >= NumClasses: # Acts as the limit for amount of classes
                break
        # Display the generated classes
        return selected_classes

if __name__ == '__main__':
    app.run(debug=True)