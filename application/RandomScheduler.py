from flask import Flask, render_template
import sqlite3

# Create an instance of the Flask class
app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('base_database.db')
cursor = conn.cursor()

# Convert Times back to how they are displayed on the original csv file
def revert_times(time):
    hour = time // 60
    minute = time % 60
    period = 'AM' if hour < 12 else 'PM'
    if hour > 12:
        hour -= 12
    return f"{hour}:{minute:02} {period}"

# Define a route to display selected classes
@app.route('/')
def display_random_classes():
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
    random_classes = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Render the template with selected classes
    return render_template('random_classes.html', classes=random_classes)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
