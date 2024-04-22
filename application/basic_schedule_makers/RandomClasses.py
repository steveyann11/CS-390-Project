import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

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

# Define the SQL query to randomly select 5 non-overlapping classes
sql_query = """
SELECT SectionName, ShortTitle, StartTime, EndTime, MeetingDays
FROM COURSEDETAILS
WHERE SectionName IN (
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

# Print the selected classes
print("Selected Classes:")
for class_info in selected_classes:
    SectionName, ShortTitle, StartTime, EndTime, MeetingDays = class_info
    print(f"Class ID: {SectionName}, Name: {ShortTitle}, Start Time: {revert_times(StartTime)}, End Time: {revert_times(EndTime)}, Meeting Days: {MeetingDays}")

# Close the database connection
conn.close()