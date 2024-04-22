import sqlite3

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

# Convert Times to number of minutes as integers so they can be compared easier
def convert_time_to_minutes(time):
    hour, minute = time.split(':')
    minute, period = minute.split(' ')
    hour = int(hour)
    minute = int(minute)
    if period == 'PM' and hour != 12:
        hour += 12
    time_to_minutes = hour * 60 + minute
    return time_to_minutes

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
    BeginTime = '8:30 AM'
    StopTime = '5:20 PM'
    days = 'MWF'
    location = "Any"
    NumClasses = 5
    return BeginTime, StopTime, days, location, NumClasses

# Assign variables preferences and convert time format
BeginTime, StopTime, days, location, NumClasses = personal_preferences()
BeginTime = convert_time_to_minutes(BeginTime)
StopTime = convert_time_to_minutes(StopTime)

# Define the SQL query to select classes based on user preferences and their corequisites
sql_query = f"""
SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cd.Coreq, cl.CampusLocation
FROM COURSEDETAILS cd
JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
WHERE cd.StartTime >= '{BeginTime}' AND cd.StartTime < '{StopTime}'
"""

#Define if statements to select classes on specific days
meeting_days = []
if 'M' in days:
    meeting_days.append("cd.MeetingDays LIKE '%M%'")
elif 'T' in days:
    meeting_days.append("cd.MeetingDays LIKE '%T%'")
elif 'W' in days:
    meeting_days.append("cd.MeetingDays LIKE '%W%'")
elif 'TH' in days:
    meeting_days.append("cd.MeetingDays LIKE '%TH%'")
elif 'F' in days:
    meeting_days.append("cd.MeetingDays LIKE '%F%'")
# Add to query
if meeting_days:
    sql_query += " AND (" + " OR ".join(meeting_days) + ")"

# Define if statements to select classes in a specific location
if location == "In Person":
    sql_query += " AND cl.CampusLocation = 'MC'"
elif location == "Online":
    sql_query += " AND cl.CampusLocation = 'OL'"

# Add ORDER BY RANDOM() and LIMIT to the main query directly
sql_query += " ORDER BY RANDOM()"

# Execute the main query
cursor.execute(sql_query)

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
    if len(selected_classes) >= NumClasses:
        break

# Print the selected classes
print("Selected Classes:")
for class_info in selected_classes:
    SectionName, ShortTitle, StartTime, EndTime, MeetingDays, Coreq, CampusLocation = class_info
    print(f"Class ID: {SectionName}, Name: {ShortTitle}, Start Time: {revert_times(StartTime)}, End Time: {revert_times(EndTime)}, Meeting Days: {MeetingDays}, Course Location: {CampusLocation}")

# Close the database connection
conn.close()
