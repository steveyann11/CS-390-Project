import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('../base_database.db')
cursor = conn.cursor()

# Convert Times back to how they are displayed on the original csv file
def revert_times(time):
    hour = time // 60
    minute = time % 60
    period = 'AM' if hour < 12 else 'PM'
    if hour > 12:
        hour -= 12
    return f"{hour}:{minute:02} {period}"


# Define the SQL query to randomly select 5 non-overlapping classes
sql_query = """
SELECT cd.SectionName, cd.ShortTitle, cd.StartTime, cd.EndTime, cd.MeetingDays, cl.CampusLocation
FROM COURSEDETAILS cd
JOIN CLASSLOCATION cl ON cd.SectionName = cl.SectionName
WHERE cd.SectionName IN (
    SELECT SectionName
    FROM COURSEDETAILS
    WHERE EndTime NOT IN (
        SELECT StartTime
        FROM COURSEDETAILS
        GROUP BY StartTime
        HAVING COUNT(*) > 1
    )
)
ORDER BY RANDOM()
LIMIT 5;
"""

# Execute the query
cursor.execute(sql_query)

# Fetch the selected classes
selected_classes = cursor.fetchall()

# Close the database connection
conn.close()

schedule = []
for class_info in selected_classes:
    SectionName, ShortTitle, StartTime, EndTime, MeetingDays, CampusLocation = class_info
    selected_class_info = (
        SectionName,
        ShortTitle,
        revert_times(StartTime),
        revert_times(EndTime),
        MeetingDays,
        CampusLocation
    )
    schedule.append(selected_class_info)

print(schedule)