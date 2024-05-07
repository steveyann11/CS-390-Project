import random

# Define major requirements (replace with actual major requirements)
major_requirements = {
    "Computer Science": ["CS-101", "CS-131", "CSL-131", "CS-132", "CSL-132", "CS-133", "CSL-133","CS-334", "CSL-334", "CS-243", "CSL-243", "CS-241", "CS-401","CS-402", "CS-491" ],
    "CS Track": ["CS-244", "CSL-244", "CS-257", "CSL-257", "CS-390", "CSL-390", "CS-254", "CSL-254", "CS-255", "CSL-255",  "CS-346", "CSL-346"],
    "Mathematics": ["MATH-107", "MATH-207", "MATH-208"],
   
}

# Generate a random schedule for a given major
def generate_schedule(major):
    schedule = {}
    for requirement, courses in major_requirements.items():
        if requirement == major:
            schedule[requirement] = random.sample(courses, k=min(len(courses), 2))  # Randomly select up to 2 courses from each requirement
        else:
            schedule[requirement] = random.sample(courses, k=1)  # Randomly select 1 course from each requirement
    return schedule

# Print a randomly generated schedule for a specific major
def print_schedule(schedule):
    for requirement, courses in schedule.items():
        print(requirement + ":")
        for course in courses:
            print("- " + course)
        print()

# Example usage
if __name__ == "__main__":
    major = "Computer Science"  # Change to desired major
    schedule = generate_schedule(major)
    print("Random Schedule for", major, "Major:")
    print_schedule(schedule)
