from flask import Flask, render_template, request
import sqlite3

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

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

# Connects the program to the webpage
@app.route('/', methods=['GET', 'POST'])
def display_schedule():
    if request.method == 'POST':
        # Get the personal preferences
        BeginTime = request.form['Start Time']
        BeginTime = convert_time_to_minutes(BeginTime)
        StopTime = request.form['End Time']
        StopTime = convert_time_to_minutes(StopTime)
        days = request.form['Days']
        location = request.form['Location']
        NumClasses = request.form['Number of Classes']

        # Create a query that will be used to gather the appropriate classes based on the users preferences
        sql_query = f"""
        SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cd.Coreq, cl.CampusLocation
        FROM COURSEDETAILS cd
        JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
        WHERE cd.StartTime >= '{BeginTime}' AND cd.StartTime < '{StopTime}'
        """

        # Define if statements to select classes on specific days


        # Define if statements to select classes in a specific location
        if location == "In Person":
            sql_query += " AND cl.CampusLocation = 'MC'"
        elif location == "Online":
            sql_query += " AND cl.CampusLocation = 'OL'"
        
        # Add ORDER BY RANDOM() to the main query directly
        sql_query += " ORDER BY RANDOM()"

        # Execute query
        cursor.execute(sql_query)
        selected_classes = cursor.fetchall()

        # Makes sure that the classes returned don't overlap and have the proper coreqs
        time_slots = []
        selected_classes = []
        for class_info in cursor.fetchall():
            SectionName, ShortTitle, StartTime, EndTime, MeetingDays, Coreq, CampusLocation = class_info
            overlap = any(start < EndTime and end > StartTime for start, end in time_slots)
            if not overlap:
                selected_classes.append(class_info)
                time_slots.append((StartTime, EndTime))
                # Check if the class has a corequisite
                if Coreq:
                    cursor.execute(f"""
                    SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cd.Coreq, cl.CampusLocation
                    FROM COURSEDETAILS cd
                    JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
                    WHERE cd.SectionName = '{Coreq}'
                    AND cd.StartTime >= ? AND cd.EndTime <= ?
                    """, (StartTime, EndTime))
                    coreq_info = cursor.fetchone()
                    if coreq_info:
                        selected_classes.append(coreq_info)
                        coreq_StartTime, coreq_EndTime = coreq_info[2], coreq_info[3]
                        time_slots.append((coreq_StartTime, coreq_EndTime))
            if len(selected_classes) >= NumClasses: # Acts as the limit for amount of classes
                break

        # Display the generated classes
