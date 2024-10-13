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

#dorm1 = Dorm(name="Nebula Hall", housing_style="Suite", capacity=140)

#create a list of dictionaries that contains the start and end room number, capacity number and occupied boolean
#nebula_room_config = [

    #first 20 rooms can fit 3 people. The next 20 rooms can fit 4 people
    #{"start": 1, "end": 20, "capacity": 3, "is_occupied": False},
    #{"start": 21, "end": 40, "capacity": 4, "is_occupied": False}
#]

#iterate through each dictionary in the list of dictionaries
#for config in nebula_room_config:

    #iterate from the start and end time specified from the dictionary
    #for i in range(config['start'], config['end'] + 1):

        #this sets a format of Rm followed by the value of i which follows a two digit format. Ex: Rm01, Rm10...
        #room_number_it = f"Rm{i:02}"

        #create a room object for each iteration
        #room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        #dorm1.add_room(room)

#this calls the __str__ method for the dorm object
#print(dorm1)
#for room in dorm1.rooms:
    #this calls the __str__ method for the room object
    #print(room)

#dorm1Dict = dorm1.to_dict()
#print(dorm1Dict)
#for room in dorm1.rooms:
    #roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm1)

#dorm2 = Dorm(name="Moonlight Hall", housing_style="Suite", capacity=30)

#moonlight_room_config = [
    #{"start": 1, "end": 10, "capacity": 1, "is_occupied": False},
    #{"start": 11, "end": 20, "capacity": 2, "is_occupied": False}
#]

#for config in moonlight_room_config:

    #for i in range(config['start'], config['end'] + 1):

        #room_number_it = f"Rm{i:02}"
        #room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        #dorm2.add_room(room)

#print(dorm2)
#for room in dorm2.rooms:
    #print(room)

#dorm2Dict = dorm2.to_dict()
#print(dorm2Dict)
#for room in dorm2.rooms:
    #roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm2)

#dorm3 = Dorm(name="Aurora Hall", housing_style="Tower", capacity=100)

#aurora_room_config = [
    #{"start": 1, "end": 10, "capacity": 1, "is_occupied": False},
    #{"start": 11, "end": 20, "capacity": 2, "is_occupied": False},
    #{"start": 21, "end": 30, "capacity": 3, "is_occupied": False},
    #{"start": 31, "end": 40, "capacity": 4, "is_occupied": False}
#]

#for config in aurora_room_config:

    #for i in range(config['start'], config['end'] + 1):

        #room_number_it = f"Rm{i:02}"
        #room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        #dorm3.add_room(room)

#print(dorm3)
#for room in dorm3.rooms:
    #print(room)

#dorm3Dict = dorm3.to_dict()
#print(dorm3Dict)
#for room in dorm3.rooms:
    #roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm3)

#dorm4 = Dorm(name="Solstice Hall", housing_style="Tower", capacity=45)

#solstice_room_config = [
    #{"start": 1, "end": 15, "capacity": 1, "is_occupied": False},
    #{"start": 16, "end": 30, "capacity": 2, "is_occupied": False}
#]

#for config in solstice_room_config:

    #for i in range(config['start'], config['end'] + 1):

        #room_number_it = f"Rm{i:02}"
        #room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        #dorm4.add_room(room)

#print(dorm4)
#for room in dorm4.rooms:
    #print(room)

#dorm4Dict = dorm4.to_dict()
#print(dorm4Dict)
#for room in dorm4.rooms:
    #roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm4)

#dorm5 = Dorm(name="Comet Hall", housing_style="Suite", capacity=210)

#comet_room_config = [
    #{"start": 1, "end": 15, "capacity": 2, "is_occupied": False},
    #{"start": 16, "end": 30, "capacity": 3, "is_occupied": False},
    #{"start": 31, "end": 45, "capacity": 4, "is_occupied": False},
    #{"start": 46, "end": 60, "capacity": 5, "is_occupied": False}
#]

#for config in comet_room_config:

    #for i in range(config['start'], config['end'] + 1):

        #room_number_it = f"Rm{i:02}"
        #room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        #dorm5.add_room(room)

#print(dorm5)
#for room in dorm5.rooms:
    #print(room)

#dorm5Dict = dorm5.to_dict()
#print(dorm5Dict)
#for room in dorm5.rooms:
    #roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm5)

dorm6 = Dorm(name="Eclipse Hall", housing_style="Tower", capacity=60)

eclipse_room_config = [
    {"start": 1, "end": 20, "capacity": 1, "is_occupied": False},
    {"start": 21, "end": 40, "capacity": 2, "is_occupied": False}
]

for config in eclipse_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_occupied = config['is_occupied'])
        dorm6.add_room(room)

print(dorm6)
for room in dorm6.rooms:
    print(room)

dorm6Dict = dorm6.to_dict()
print(dorm6Dict)
for room in dorm6.rooms:
    roomDict = room.to_dict()
    print(roomDict)

add_dorm(dorm6)