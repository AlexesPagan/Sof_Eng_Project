import firebase_admin
from firebase_admin import credentials, firestore

# Path to the service account JSON file
cred = credentials.Certificate("C:/Users/ajero/databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
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
#new_student = collect_student_info()
#add_student(new_student)
#print("All students:")
#get_students()

#This class defines all data that represents a Dorm Building
class Dorm:

    #This method acts as a constructor and assigns these attributes to each dorm object
    def __init__(self, name, housing_style, capacity):
        self.name = name
        self.housing_style = housing_style
        self.capacity = capacity
        self.rooms = []

    #This nested class defines all data that represents the different rooms within a dorm
    class Room:

        #This method acts as a constructor and assigns these attributes to each room object
        def __init__(self, room_number, capacity, is_occupied=False):
            self.room_number = room_number
            self.capacity = capacity
            self.is_occupied = is_occupied

        #This method converts the data of the room into a dictionary format
        def to_dict(self):
            return {
                'room_number': self.room_number,
                'capacity': self.capacity,
                'is_occupied': self.is_occupied
            }

        #This method displays room data as a string
        def __str__(self):
            return f"Room Number: {self.room_number}, Capacity: {self.capacity}, Occupied: {self.is_occupied}"

    #This method adds a new room object to the list of rooms
    def add_room(self, room):
        self.rooms.append(room)

    #This method converts the data of the dorm into a dictionary format
    def to_dict(self):
        return {
            'name': self.name,
            'housing_style': self.housing_style,
            'capacity': self.capacity,
            'rooms': [room.to_dict() for room in self.rooms]  # Include room info
        }

    #This method displays the data of the dorm as a string
    def __str__(self):
        return f"Dorm Name: {self.name}, Style: {self.housing_style}, Capacity: {self.capacity}"

#This method adds a dorm to the database
def add_dorm(dorm):
    db.collection('dorms').add(dorm.to_dict())
    print(f"Added dorm: {dorm.name}")

#Testing
dorm1 = Dorm(name="Nebula Hall", housing_style="Suite", capacity=200)

#names for future dorms: moonlight hall, aurora hall, solstice hall, comet hall, eclipse hall
room1 = Dorm.Room(room_number="Rm01", capacity=2, is_occupied=False)
room2 = Dorm.Room(room_number="Rm02", capacity=3, is_occupied=False)
room3 = Dorm.Room(room_number="Rm03", capacity=2, is_occupied=True)

dorm1.add_room(room1)
dorm1.add_room(room2)
dorm1.add_room(room3)

#this calls the __str__ method for the dorm object
print(dorm1)
for room in dorm1.rooms:
    #this calls the __str__ method for the room object
    print(room)

dorm1Dict = dorm1.to_dict()
print(dorm1Dict)
for room in dorm1.rooms:
    roomDict = room.to_dict()
    print(roomDict)

add_dorm(dorm1)
