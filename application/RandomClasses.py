import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Define the SQL query to randomly select 5 non-overlapping classes
sql_query = """
SELECT id, class_name, start_time, end_time
FROM classes
WHERE id IN (
    SELECT id
    FROM classes
    WHERE start_time NOT IN (
        SELECT start_time
        FROM classes
        GROUP BY start_time
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
    class_id, class_name, start_time, end_time = class_info
    print(f"Class ID: {class_id}, Name: {class_name}, Start Time: {start_time}, End Time: {end_time}")

# Close the database connection
conn.close()