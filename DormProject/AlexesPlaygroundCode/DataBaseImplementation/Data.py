import firebase_admin
from firebase_admin import credentials, firestore

# Path to the service account JSON file
cred = credentials.Certificate("C:/Users/ajero/databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

#print("Firebase connected!")
#print("Hello pycharm")

#This class defines all data that represents a student
class Student:

    #This method acts as a constructor and assigns these attributes for each student object
    def __init__(self, name, student_id, year, handicaps, preferences):
        self.name = name
        self.student_id = student_id
        self.year = year
        self.handicaps = handicaps
        self.preferences = preferences

    #This method converts the student data into a dictionary format
    def to_dict(self):
        return {
            'name': self.name,
            'student_id': self.student_id,
            'year': self.year,
            'handicaps': self.handicaps,
            'preferences': self.preferences
        }

#This method adds a student to the database
def add_student(student):
    db.collection('students').add(student.to_dict())
    print(f"Added student: {student.name}")

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

#This method asks the user general data questions and creates a student object with it
def collect_student_info():
    name = input("Enter your name: ")
    student_id = input("Enter your student ID: ")
    year = input("Enter your year (e.g., Freshman, Sophomore, etc.): ")
    handicaps = input("Enter any handicaps (separate by commas, or type 'None'): ")

    #check if the user inputted no handicaps
    #strip() gets rid of unnecessary whitespace. lower() changes string to lowercase
    if handicaps.strip().lower() == 'none':
        handicaps = []

    #user inputted a handicap
    #split() is used to separate strings based on commas
    else:
        handicaps = [h.strip() for h in handicaps.split(',')]

    preferences = input("Enter your preferences (separate by commas): ")
    preferences = [p.strip() for p in preferences.split(',')]

    #create a new student object with provided data
    return Student(name, student_id, year, handicaps, preferences)

#Testing
new_student = collect_student_info()
add_student(new_student)
print("All students:")
get_students()

#class Dorms:
    #def __init__(self):

    #class Rooms:
        #def __init__(self):

        #def to_dict(self):

    #def add_room(self):

    #def to_dict(self):

#Testing