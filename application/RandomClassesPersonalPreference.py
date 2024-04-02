import sqlite3

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

# Convert Times to a 24-hour format as integers so they can be compared easier
def convert_time_decimal(time):
    hour, minute = time.split(':')
    minute, period = minute.split(' ')
    hour = int(hour)
    minute = int(minute)
    if period == 'PM' and hour != 12:
        hour += 12
    time_decimal = hour * 60 + minute
    return time_decimal

# Convert Times back to how they are displayed on the original csv file
def revert_times(time):
    hour = time // 60
    minute = time % 60
    if hour < 12:
        period = 'AM'
    elif hour >= 12:
        period = 'PM'
        if hour > 12:
            hour = hour - 12
    return f"{hour}:{minute:02} {period}"

# Simulated user inputs
def personal_preferences():
    BeginTime = 480
    StopTime = 1020
    days = "'MWF'"
    location = "In Person"
    NumClasses = 5
    return BeginTime, StopTime, days, location, NumClasses


# Assign variables preferences and convert time format
BeginTime, StopTime, days, location, NumClasses = personal_preferences()


# Define the SQL query to select classes based on user preferences
sql_query = f"""
SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cl.CampusLocation
FROM COURSEDETAILS cd
JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
WHERE cd.StartTime >= '{BeginTime}' AND cd.StartTime < '{StopTime}'
AND cd.MeetingDays = {days}
"""

# Define if statements to select classes in a specific location
if location == "In Person":
    sql_query += " AND cl.CampusLocation = 'MC'"
elif location == "Online":
    sql_query += " AND cl.CampusLocation = 'OL'"

# Add ORDER BY RANDOM() and LIMIT to the main query directly
sql_query += f" ORDER BY RANDOM() LIMIT {NumClasses}"

# Execute the main query
cursor.execute(sql_query)

# Fetch the selected classes
selected_classes = cursor.fetchall()

# Print the selected classes
print("Selected Classes:")
for class_info in selected_classes:
    SectionName, ShortTitle, StartTime, EndTime, MeetingDays, CampusLocation = class_info
    print(f"Class ID: {SectionName}, Name: {ShortTitle}, Start Time: {revert_times(StartTime)}, End Time: {revert_times(EndTime)}, Meeting Days: {MeetingDays}, Course Location: {CampusLocation}")

# Close the database connection
conn.close()
