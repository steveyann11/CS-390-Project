from flask import Flask, render_template, request
import sqlite3
import random

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

# Connects the program to the webpage
@app.route('/calendar', methods=['GET', 'POST'])
def display_schedule():
    if request.method == 'POST':

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

        # Display the generated classes
        return render_template('calendar.html', result=selected_classes)
    else:
        return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)