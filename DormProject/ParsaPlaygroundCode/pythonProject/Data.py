import firebase_admin
from firebase_admin import credentials, firestore
import re

# Path to the service account JSON file
cred = credentials.Certificate("C:/Users/PJ/Desktop/Key/databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

#This class defines all data that represents a student
class Student:

    #This method acts as a constructor and assigns these attributes for each student object
    def __init__(self, name, student_id, year, handicaps, preferences, email, password):
        self.name = name
        self.student_id = student_id
        self.year = year
        self.handicaps = handicaps
        self.preferences = preferences
        self.email = email,
        self.password = password

    #This method converts the student data into a dictionary format
    def to_dict(self):
        return {
            'name': self.name,
            'student_id': self.student_id,
            'year': self.year,
            'handicaps': self.handicaps,
            'preferences': self.preferences,
            'email': self.email,
            'password': self.password
        }

#This method asks the user general data questions and creates a student object with it
def collect_student_info():
    name, student_id, year, email, password = get_validated_input()
    handicaps, preferences = get_handicaps_preferences()
    return Student(name, student_id, year, handicaps, preferences, email, password)

def get_validated_input():
    name = validate_name()
    student_id = validate_student_id()
    year = validate_year()
    email = validate_email()
    password = validate_password()
    return name, student_id, year, email, password

# Validating the name
def validate_name():
    while True:
        name = input("Enter your name: ")
        if re.match(r'^[A-Za-z ]+$', name):
            return name
        print("Invalid name. Please use only letters and spaces.")

# Validating the student ID
def validate_student_id():
    while True:
        student_id = input("Enter your student ID: ")
        if re.match(r'^H\d{9}$', student_id):
            return student_id
        print("Invalid ID. Format should be 'H' followed by 9 digits.")

# Validating the year
def validate_year():
    valid_years = ['freshman', 'sophomore', 'junior', 'senior']
    while True:
        year = input("Enter your year (e.g., Freshman, Sophomore, etc.): ")
        if year.lower() in valid_years:
            return year
        print("Invalid year. Enter a valid year name like Freshman, Senior...")

# Validating the email
def validate_email():
    while True:
        email = input("Enter your email: ")
        if re.match(r'^[a-zA-Z0-9._]+@pride\.hofstra\.edu$', email):
            return email
        print("Invalid email format. Please enter a valid email.")

# Validating the password
def validate_password():
    while True:
        password = input("Enter your password: ")
        if len(password) >= 6:
            return password
        print("Password must be at least 6 characters long.")

# Validating the handicaps and preferences
def get_handicaps_preferences():
    handicaps = input("Enter any handicaps (separate by commas, or type 'None'): ")
    if handicaps.strip().lower() == 'none':
        handicaps = []
    else:
        handicaps = [h.strip() for h in handicaps.split(',')]
    preferences = input("Enter your preferences (separate by commas): ")
    preferences = [p.strip() for p in preferences.split(',')]
    return handicaps, preferences

#This method adds a student to the database
def add_student(student):
    db.collection('students').add(student.to_dict())
    print(f"Added student: {student.name}")

# This method updates the student's information, by passing the student's ID and the updated data
def update_student(student_id, update_data):

    # Sets a reference to the database
    students_ref = db.collection('students')

    # Query to find the student by ID
    result = students_ref.where('student_id', '==', student_id).stream()

    for student in result:
        # Updating the student document
        db.collection('students').document(student.id).update(update_data)
        print(f"Updated student with ID {student_id}")

# This method deletes the student object from the data by passing the student ID
def delete_student(student_id):
    # Sets a reference to the database
    students_ref = db.collection('students')

    # Query to find the student by ID
    result = students_ref.where('student_id', '==', student_id).stream()

    for student in result:
        # Delete the specific student found by the query
        db.collection('students').document(student.id).delete()
        print(f"Deleted student with ID {student_id}")

#This method retrieves all students from the database
def get_students():

    #sets a reference to the database
    students_ref = db.collection('students')

    #use stream() in order to get all data from the database reference
    students = students_ref.stream()

    #iterate through the entire database
    for student in students:

        #prints the unique document id for each collection of data followed by that students data
        print(f"{student.id} => {student.to_dict()}")



# Testing the functionalities
print("Registering new student...")
new_student = collect_student_info()
add_student(new_student)

print("Current students: ")
get_students()

# Example update data
update_data = {'year': 'Junior', 'preferences': ['quiet', 'library']}
print("Updating student information...")
update_student(new_student.student_id, update_data)

print("Updated students: ")
get_students()

print("Deleting a student...")
delete_student(new_student.student_id)

print("Students after deletion: ")
get_students()


#class Dorms:
    #def __init__(self):

    #class Rooms:
        #def __init__(self):

        #def to_dict(self):

    #def add_room(self):

    #def to_dict(self):

#Testing