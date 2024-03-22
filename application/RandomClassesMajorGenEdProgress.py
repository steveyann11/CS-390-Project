import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

# Finds what required classes the user needs to take that are offered in the semester
def req_classes():
    # Rest of code depends on how we plan on getting the Users progress
    # This should take into account prereq so classes that cannot be taken are not offered.


# Assign variables for the classes
= req_classes()

# Define the SQL query to select classes based on user preferences
# Insert the specific variables following the WHERE statement
sql_query = """
SELECT SectionName, ShortTitle, StartTime, EndTime, MeetingDays
FROM COURSEDETAILS
WHERE 

ORDER BY RANDOM()
LIMIT 5;
"""

# Execute the query with personal preferences
cursor.execute(sql_query, ())

# Fetch the selected classes
selected_classes = cursor.fetchall()

# Print the selected classes
print("Selected Classes:")
for class_info in selected_classes:
    SectionName, ShortTitle, StartTime, EndTime, MeetingDays = class_info
    print(f"Class ID: {SectionName}, Name: {ShortTitle}, Start Time: {StartTime}, End Time: {EndTime}, Meeting Days: {MeetingDays}")

# Close the database connection
conn.close()
