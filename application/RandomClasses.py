import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

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
    print(f"Class ID: {SectionName}, Name: {ShortTitle}, Start Time: {StartTime}, End Time: {EndTime}, Meeting Days: {MeetingDays}")

# Close the database connection
conn.close()