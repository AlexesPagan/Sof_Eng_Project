import firebase_admin
from firebase_admin import credentials, firestore

# Path to the service account JSON file
cred = credentials.Certificate("C:/Users/PJ/Desktop/Key/databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

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

#This method asks the user general data questions and creates a student object with it
def collect_student_info():
    name = input("Enter your name: ")
    student_id = input("Enter your student ID: ")
    year = input("Enter your year (e.g., Freshman, Sophomore, etc.): ")
    handicaps = input("Enter any handicaps (separate by commas, or type 'None'): ") # ***Future solution that leverages Machine Learning to summarize the important part of the text***

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