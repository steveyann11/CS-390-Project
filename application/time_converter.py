# Convert Times to a 24-hour format as integers so they can be compared easier
def convert_time_to_minutes(time):
    '''
    Input: A string with time in the 12 hour format (9:30 AM)
    Output: An integer that represents the number of minutes for that specific time
    '''
    hour, minute = time.split(':')
    minute, period = minute.split(' ')
    hour = int(hour)
    minute = int(minute)
    if period == 'PM' and hour != 12:
        hour += 12
    time_to_minutes = hour * 60 + minute
    return time_to_minutes