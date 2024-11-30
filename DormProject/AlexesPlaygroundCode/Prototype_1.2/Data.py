# REVISION HISTORY
# Parsa     10/20/2024  Added the Admin class, refined the user role logic, and improved input validation for a streamlined and error-free user experience.
# Parsa     10/20/2024  Implemented synchronization between Firestore and Firebase Authentication to ensure that each user's Firestore document ID is used as their Firebase Authentication UID upon creation.
# Alexes    10/26/2024  Modified Dorm data to include specific fata fields such as if a room has accessibility accommodations or not as well as a list of students to illustrate who is assigned to what room.
# Alexes    10/26/2024  Added room assignment functions to add or remove students to specified rooms in a dorm
# Alexes    10/26/2024  Adjusted dorm data testing code to update our firestore database based on the previous changes I implemented
# Alexes    10/28/2024  Added the get_response() function to retrieve all data from the form_responses collection in our firestore
# Alexes    10/28/2024  Added the trim_response_data() function to remove any invalid form response data from the form_responses collection
# Alexes    11/29/2024  Added the get_student_in_dorm(dorm_name) function to return as a list all id's of the students residing in those dorms, this includes roommate id's.
# Alexes    11/29/2024  Created the add_or_remove_student function that provides the backend functionality for allowing admins to add or remove students from a dorm room. It takes 4 different parameters including the dorm name, room number, student id, and role (add or remove). This function also updates the firestore database to visualize the changes.



import firebase_admin
from firebase_admin import credentials, firestore, auth
import re

# Path to the service account JSON file
cred = credentials.Certificate("C:/Users/ajero/databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
firebase_admin.initialize_app(cred)

# Initialize Firestore

db = firestore.client()


class User:
    def __init__(self, name, user_id, email, role):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            'name': self.name,
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role
        }


#This class defines all data that represents a student
class Student(User):

    #This method acts as a constructor and assigns these attributes for each student object
    def __init__(self, name, user_id, email, role, year, handicaps, preferences):
        super().__init__(name, user_id, email, role)
        self.year = year
        self.handicaps = handicaps
        self.preferences = preferences

    #This method converts the student data into a dictionary format
    def to_dict(self):
        student_dict = super().to_dict()
        student_dict.update({
            'year': self.year,
            'handicaps': self.handicaps,
            'preferences': self.preferences,
        })
        return student_dict

class Admin(User):
    def __init__(self, name, user_id, email, role):
        super().__init__(name, user_id, email, role)

    def change_room_assignment(self, student_id, new_room):
        # Logic to change the room assignment in Firestore
        print(f"Changing room for student {student_id} to {new_room}")


    def view_student_info(self, student_id):
        # Logic to retrieve and view detailed student information for matching or status updates
        print(f"Viewing information for student {student_id}")
        # This method would interact with Firestore to retrieve detailed student information

    def cancel_room_request(self, student_id):
        # Logic to cancel a room request
        print(f"Cancelling room request for student {student_id}")
        # Method to handle the cancellation process in Firestore

    def update_room_status(self, room_id, new_status):
        # Logic to update the status of a room
        print(f"Updating status of room {room_id} to {new_status}")
        # This would change the availability status of a room in the Firestore database

# User creation with role management
def create_user():
    role = input("Enter 'admin' for Admin, 'student' for Student: ")
    if role == 'student':
        return create_student()
    elif role == 'admin':
        return create_admin()

def create_student():
    name = validate_name()
    user_id = validate_user_id()
    email = validate_email()
    year = validate_year()
    handicaps, preferences = get_handicaps_preferences()
    student = Student(name, user_id, email, 'student', year, handicaps, preferences)
    add_user(student)
    return student

def create_admin():
    name = validate_name()
    user_id = validate_user_id()
    email = validate_email()
    admin = Admin(name, user_id, email, 'admin')
    add_user(admin)
    return admin

# Input validation based on role
#def get_validated_input(role):
    #name = validate_name()
    #user_id = validate_user_id()
    #email = validate_email()
    #if role == 'student':
        #year = validate_year()
        #handicaps, preferences = get_handicaps_preferences()
    #else:
        #year, handicaps, preferences = None, [], []
    #return name, user_id, email, year, handicaps, preferences

def validate_name():
    while True:
        name = input("Enter your name: ")
        if re.match(r'^[A-Za-z ]+$', name):
            return name
        print("Invalid name. Please use only letters and spaces.")

def validate_user_id():
    while True:
        user_id = input("Enter your user ID: ")
        if re.match(r'^H\d{9}$', user_id):
            return user_id
        print("Invalid ID. Format should be 'H' followed by 9 digits.")

def validate_year():
    valid_years = ['freshman', 'sophomore', 'junior', 'senior']
    while True:
        year = input("Enter your year (e.g., Freshman, Sophomore, etc.): ")
        if year.lower() in valid_years:
            return year
        print("Invalid year. Enter a valid year name like Freshman, Senior...")

def validate_email():
    while True:
        email = input("Enter your email: ")
        if re.match(r'^[a-zA-Z0-9._]+@pride\.hofstra\.edu$', email):
            return email
        print("Invalid email format. Please enter a valid email.")

def get_handicaps_preferences():
    handicaps = input("Enter any handicaps (separate by commas, or type 'None'): ")
    if handicaps.strip().lower() == 'none':
        handicaps = []
    else:
        handicaps = [h.strip() for h in handicaps.split(',')]
    preferences = input("Enter your preferences (separate by commas): ")
    return handicaps, [p.strip() for p in preferences.split(',')]

# Add, update, delete, and get users
def add_user(user):
    # First, adding the user to Firestore and get the document reference
    doc_ref = db.collection(user.role + 's').add(user.to_dict())[1]  # This returns the document reference
    print(f"Added {user.role}: {user.name} with Firestore ID {doc_ref.id}")

    # Now, asking for a password and create the user in Firebase Authentication
    password = input(f"Enter a password for {user.email}: ")
    create_firebase_user(user.email, password, user.name, user.role, doc_ref.id)

def create_firebase_user(email, password, name, role, doc_id):
    # Create the user in Firebase Authentication using the Firestore document ID as the UID
    try:
        user = auth.create_user(
            uid=doc_id,
            email=email,
            password=password,
            display_name=name
        )
        print('Successfully created new user for Firebase Authentication:', user.uid)
    except Exception as e:
        print(f"Failed to create Firebase user: {e}")

def update_user_info(user_id, update_data):
    collection = 'admins' if user_id.startswith('A') else 'students'
    user_doc = db.collection(collection).where('user_id', '==', user_id).get()
    for doc in user_doc:
        doc.reference.update(update_data)
        print(f"Updated {collection[:-1]} with ID {user_id}")

def delete_user(user_id, role):
    collection = 'admins' if role == 'admin' else 'students'
    user_doc = db.collection(collection).where('user_id', '==', user_id).get()
    for doc in user_doc:
        doc.reference.delete()
        print(f"Deleted {role} with ID {user_id}")

def get_users():
    print("Getting users: ")
    collection = 'admins' if input("Enter 'a' for admins, any other key for students: ").lower() == 'a' else 'students'
    users = db.collection(collection).stream()
    for user in users:
        print(f"{user.id} => {user.to_dict()}")

# Main execution
#new_user = create_user()

# Role-specific actions
#if isinstance(new_user, Admin):
    #new_user.view_student_info('S123')
    #new_user.change_room_assignment('S123', 'Room 102')
#elif isinstance(new_user, Student):
    #update_data = {'year': 'Junior', 'preferences': ['quiet', 'library']}
    #update_user_info(new_user.user_id, update_data)

#get_users()
#delete_user(new_user.user_id, new_user.role)

#This class defines all data that represents a Dorm Building
class Dorm:

    #This method acts as a constructor and assigns these attributes to each dorm object
    def __init__(self, name, housing_style, capacity):
        self.name = name
        self.housing_style = housing_style
        self.capacity = capacity
        self.rooms = []

    #future updates to the room class: create a list with predefined size that holds student names. This will allow for easier integration between data and dorm application down the line
    #This nested class defines all data that represents the different rooms within a dorm
    class Room:

        #This method acts as a constructor and assigns these attributes to each room object
        def __init__(self, room_number, capacity, is_occupied=False, is_accessible=False):
            self.room_number = room_number
            self.capacity = capacity
            self.is_occupied = is_occupied #tells us if the room is full or not
            self.is_accessible = is_accessible #tells us if the room has accessibility accommodations
            self.students = [] #list that tells us what students are assigned to the room

        #this function adds a student to the room if there is room
        def add_student(self, student):

            #if length of the list of students in the room is < the size of the room
            if len(self.students) < self.capacity:

                #add student to the list for the room
                self.students.append(student)

                #if capacity is at max, set room to occupied
                if (len(self.students) == self.capacity):
                    self.is_occupied = True

            else:
                print("Room is already occupied")

        #this function removes a student from the list of students assigned to the room by using the student id
        def remove_student(self, student_id):

            #update the list of students for the room by iterating over the current list and excluding the student with the specified id
            self.students = [s for s in self.students if s.user_id != student_id]

            #if the list is empty, the room isn't occupied
            if not self.students:
                self.is_occupied = False

        #This method converts the data of the room into a dictionary format
        def to_dict(self):
            return {
                'room_number': self.room_number,
                'capacity': self.capacity,
                'is_occupied': self.is_occupied,
                'is_accessible': self.is_accessible,
                'students': [student.to_dict().get('name', 'Unknown') for student in self.students]
            }

        #This method displays room data as a string
        def __str__(self):

            #get only the names from the list of students. if no nmae is present, it will display unknown
            student_names = [student.to_dict().get('name', 'Unknown') for student in self.students]

            return (f"Room Number: {self.room_number}, Capacity: {self.capacity}, Occupied: {self.is_occupied}, Accessibility: {self.is_accessible}, Students: {student_names}")

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

def get_students():

    #sets a reference to the database
    students_ref = db.collection('students')

    #use stream() in order to get all data from the database reference
    students = students_ref.stream()

    student_list = []

    #iterate through the entire database
    for student in students:
        student_list.append(student)

    return student_list

#function that stores as a list all id's for all students in a given dorm
def get_students_in_dorm(dorm_name):

    #set a reference to a specified dorm in the dorm collection
    dorm_ref = db.collection('dorms').where('name', '==', dorm_name).stream()

    #create a list to store student id's
    student_ids = []

    #transform the dorm data into a readable dictionary format
    for dorm in dorm_ref:
        dorm_data = dorm.to_dict()

        #iterate through all rooms of the dorm
        for rooms in dorm_data.get('rooms', []):

            #iterate through the student list for each room
            for students in rooms.get('students', []):

                #find and add all the id's within each rooms student list.
                student_id = students.get('ID')

                #if the data for the student id is found, add the id to the list of id's
                if student_id:
                    student_ids.append(student_id)

    #return the list of id's
    return student_ids

#function that will either add or remove a specified student from a dorm room.
#all excluded print statements are just used for testing purposes
def add_or_remove_student(dorm_name, room_number, student_id, task):

    #print(dorm_name)
    #print(room_number)
    #print(student_id)
    #print(task)

    #set a reference to a specified dorm in the dorm collection
    dorm_ref = db.collection('dorms').where('name', '==', dorm_name).stream()

    #print('entering first iteration')

    #transform the dorm data into a readable dictionary format
    for dorm in dorm_ref:
        dorm_data = dorm.to_dict()

        #keep a reference to the document id for the specific dorm
        dorm_id = dorm.id

        #print("entering second iteration")

        #iterate through all rooms of the dorm until a match is found
        for rooms in dorm_data.get('rooms', []):

            #if the current room is the room specified in the parameter
            if rooms.get('room_number') == room_number:
                #print("found room")

                #access the student list in the specified room
                students = rooms.get('students', [])

                #print("entering student list in room")

                if task == "Add":

                    print("adding student")

                    #add the specified student id to the student list and then call firebase to update the data of the specified document id
                    students.append({"ID": student_id})
                    db.collection('dorms').document(dorm_id).update({'rooms': dorm_data['rooms']})

                elif task == "Remove":
                    print("removing student")

                    #we "remove" the student by creating a new list of students excluding the student with the id we want to remove
                    updated_students = [student for student in students if student.get('ID') != student_id]

                    #locally update the data for the dorm and then update the data on the database to match with the local data
                    rooms['students'] = updated_students
                    db.collection('dorms').document(dorm_id).update({'rooms': dorm_data['rooms']})

    print("done")


#Testing

test_dorm = Dorm(name="Test Dorm", housing_style="suite", capacity=25)

room_configs = [
    {"room_number": "RM01", "capacity": 2, "is_accessible": False},
    {"room_number": "Rm02", "capacity": 3, "is_accessible": True},
    {"room_number": "Rm03", "capacity": 1, "is_accessible": False},
    {"room_number": "Rm04", "capacity": 2, "is_accessible": True},
    {"room_number": "Rm05", "capacity": 3, "is_accessible": False},
    {"room_number": "Rm06", "capacity": 4, "is_accessible": True},
    {"room_number": "Rm07", "capacity": 1, "is_accessible": False},
    {"room_number": "Rm08", "capacity": 2, "is_accessible": False},
    {"room_number": "Rm09", "capacity": 3, "is_accessible": True},
    {"room_number": "Rm10", "capacity": 4, "is_accessible": False}
]

for config in room_configs:
    room = Dorm.Room(room_number=config["room_number"], capacity=config["capacity"], is_accessible=config["is_accessible"])
    test_dorm.add_room(room)

#test_student = get_students()
#print (test_student)

# assign students to rooms
#for student_data in test_student:
#    for room in test_dorm.rooms:

#        if not room.is_occupied:
#            room.add_student(student_data)
            #once the student is added, move onto the next student
#            break

#print(test_dorm)

#for room in test_dorm.rooms:
    #print(room)

#add_dorm(test_dorm)
#-------------------------------------------------------------------------------
#Testing get_students_in_dorm and add_or_remove_student functions

#students_in_dorm = get_students_in_dorm("Comet Hall")

#for student in students_in_dorm:
    #print(student)

#add_or_remove_student("Test Dorm", "Rm06", "H777777777", "Add")

add_or_remove_student("Test Dorm", "Rm06", "H777777777", "Remove")

#------------------------------------------------------------------------------------
#Updating our current dorm data

dorm1 = Dorm(name="Nebula Hall", housing_style="Suite", capacity=75)

#create a list of dictionaries that contains the start and end room number, capacity number and occupied boolean
nebula_room_config = [

    #first 20 rooms can fit 3 people. The next 20 rooms can fit 4 people
    {"start": 1, "end": 5, "capacity": 1, "is_accessible": False},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

#iterate through each dictionary in the list of dictionaries
for config in nebula_room_config:

    #iterate from the start and end time specified from the dictionary
    for i in range(config['start'], config['end'] + 1):

        #this sets a format of Rm followed by the value of i which follows a two digit format. Ex: Rm01, Rm10...
        room_number_it = f"Rm{i:02}"

        #create a room object for each iteration
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm1.add_room(room)

#this calls the __str__ method for the dorm object
#print(dorm1)
#for room in dorm1.rooms:
    #this calls the __str__ method for the room object
    #print(room)

dorm1Dict = dorm1.to_dict()
#print(dorm1Dict)
for room in dorm1.rooms:
    roomDict = room.to_dict()
    #print(roomDict)

#add_dorm(dorm1)

dorm2 = Dorm(name="Moonlight Hall", housing_style="Suite", capacity=75)

moonlight_room_config = [
    {"start": 1, "end": 5, "capacity": 1, "is_accessible": True},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

for config in moonlight_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm2.add_room(room)

#print(dorm2)
#for room in dorm2.rooms:
#    print(room)

dorm2Dict = dorm2.to_dict()
#print(dorm2Dict)
for room in dorm2.rooms:
    roomDict = room.to_dict()
#    print(roomDict)

#add_dorm(dorm2)

dorm3 = Dorm(name="Aurora Hall", housing_style="Tower", capacity=75)

aurora_room_config = [

    {"start": 1, "end": 5, "capacity": 1, "is_accessible": True},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

for config in aurora_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm3.add_room(room)

#print(dorm3)
#for room in dorm3.rooms:
#    print(room)

dorm3Dict = dorm3.to_dict()
#print(dorm3Dict)
for room in dorm3.rooms:
    roomDict = room.to_dict()
#    print(roomDict)

#add_dorm(dorm3)

dorm4 = Dorm(name="Solstice Hall", housing_style="Tower", capacity=75)

solstice_room_config = [
    {"start": 1, "end": 5, "capacity": 1, "is_accessible": True},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

for config in solstice_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm4.add_room(room)

#print(dorm4)
#for room in dorm4.rooms:
#    print(room)

dorm4Dict = dorm4.to_dict()
#print(dorm4Dict)
for room in dorm4.rooms:
    roomDict = room.to_dict()
#    print(roomDict)

#add_dorm(dorm4)

dorm5 = Dorm(name="Comet Hall", housing_style="Suite", capacity=75)

comet_room_config = [
    {"start": 1, "end": 5, "capacity": 1, "is_accessible": False},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

for config in comet_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm5.add_room(room)

#print(dorm5)
#for room in dorm5.rooms:
#    print(room)

dorm5Dict = dorm5.to_dict()
#print(dorm5Dict)
for room in dorm5.rooms:
    roomDict = room.to_dict()
#    print(roomDict)

#add_dorm(dorm5)

dorm6 = Dorm(name="Eclipse Hall", housing_style="Tower", capacity=75)

eclipse_room_config = [
    {"start": 1, "end": 5, "capacity": 1, "is_accessible": False},
    {"start": 6, "end": 10, "capacity": 2, "is_accessible": False},
    {"start": 11, "end": 15, "capacity": 3, "is_accessible": False},
    {"start": 16, "end": 20, "capacity": 4, "is_accessible": False},
    {"start": 21, "end": 25, "capacity": 5, "is_accessible": False}
]

for config in eclipse_room_config:

    for i in range(config['start'], config['end'] + 1):

        room_number_it = f"Rm{i:02}"
        room = Dorm.Room(room_number=room_number_it, capacity = config['capacity'], is_accessible = config['is_accessible'])
        dorm6.add_room(room)

#print(dorm6)
#for room in dorm6.rooms:
#    print(room)

dorm6Dict = dorm6.to_dict()
#print(dorm6Dict)
for room in dorm6.rooms:
    roomDict = room.to_dict()
#    print(roomDict)

#add_dorm(dorm6)
#--------------------------------------------------------------------------------------------------------

# function to get all responses from the form_responses collection
def get_responses():

    #I realized this line of code does the exact same job as the get_students function
    return db.collection('form_responses').stream()

#function that compares each id for all responses in the form_responses collection with all ids in the students collection. Removes any invalid response data
def trim_response_data():
    # get all data from student collection
    student_example = get_students()

    # create a dictionary of the student data containing only their student id
    student_id_test = [student.to_dict().get('user_id', 'Unknown') for student in student_example]
    print(student_id_test)

    # get all data from the form_responses collection
    response_example = get_responses()

    # create a list of tuples which includes the id from the form response and the firestore document reference to that response
    response_data = [(response.to_dict().get("ID", "Unknown"), response.reference) for response in response_example]

    # create a list taking only the id data from response_data
    response_ids = [response[0] for response in response_data]
    print(response_ids)

    #iterate through each tuple in the list of tuples
    for response_id, reference in response_data:

        #variable to signify a valid id comparison
        valid_data = False

        #iterate through each student id
        for id in student_id_test:

            print(f"comparing {response_id} with {id}")

            #if the id specified in the form does not match the student id, it is an invalid id
            if response_id != id:
                print(f"valid id: {valid_data}")

            #if the id specified in the form does match, it is a valid id. Break to exit this for loop
            else:
                valid_data = True
                print(f"valid id: {valid_data}")
                break

        print("Comparison completed")

        if valid_data == False:
            print(f"No match was found. {response_id} is an invalid id. Deleting")

            #remove the invalid response data by deleting the firestore document in the form_responses collection
            reference.delete()

    print("Trimming is complete, all invalid responses were deleted")

#Testing
#trim_response_data()

#---------------------------------------------------------------------------------------------------------

#function that takes as a parameter the name of a dorm, and the numbered choice of that dorm. ex: (Comet Hall, 1st)
#this function only works for students who have the RSS choices with exception for people with RA choices as RA refers to accommodation students. This is meant for the dorms with the suite housing style
def get_students_by_dorm_choice_suite(dorm_name, choice_number):

    #create a reference key based on the choice_number parameter
    dorm_key = f"{choice_number}RSS_dorm_choice"
    dorm_key2 = f"{choice_number}RA_dorm_choice"

    #create a list of all the form responses in a dictionary format
    response_data = [response.to_dict() for response in db.collection('form_responses').stream()]

    #create a new list of only the form responses who have the same numbered dorm choice. ex: a list of only students who chose Comet Hall as their 1st choice
    filtered_students = [data for data in response_data if data.get(dorm_key) == dorm_name]
    filtered_accommodated_students = [data for data in response_data if data.get(dorm_key2) == dorm_name]

    for student in filtered_accommodated_students:
        filtered_students.append(student)

    return filtered_students

#function that takes as a parameter the name of a dorm, and the numbered choice of that dorm. ex: (Aurora Hall, 1st)
#this function only works for students who have the RST choices with exception for people with RA choices as RA refers to accommodation students. This is meant for the dorms with the tower housing style
def get_students_by_dorm_choice_tower(dorm_name, choice_number):

    # create a reference key based on the choice_number parameter
    dorm_key = f"{choice_number}RST_dorm_choice"
    dorm_key2 = f"{choice_number}RA_dorm_choice"

    # create a list of all the form responses in a dictionary format
    response_data = [response.to_dict() for response in db.collection('form_responses').stream()]

    # create a new list of only the form responses who have the same numbered dorm choice. ex: a list of only students who chose Aurora Hall as their 1st choice
    filtered_students = [data for data in response_data if data.get(dorm_key) == dorm_name]
    filtered_accommodated_students = [data for data in response_data if data.get(dorm_key2) == dorm_name]

    for student in filtered_accommodated_students:
        filtered_students.append(student)

    return filtered_students

#function to display all data of the given list of dictionaries, specifically for the two functions above
def display_student_data(students):
  #iterate through the list of dictionaries
    for student in students:

        #case of student applying for dorm with suite style
        if student.get("Accomodations") == "No, I do not require accommodations" and student.get("House_Style") == "Suite style":
            print("student data")
            print("ID:", student.get("ID"))
            print("1st Dorm Choice:", student.get("1stRSS_dorm_choice"))
            print("1st Room Choice:", student.get("1stRSS_room_choice"))
            print("2nd Dorm Choice:", student.get("2ndRSS_dorm_choice"))
            print("2nd Room Choice:", student.get("2ndRSS_room_choice"))
            print("3rd Dorm Choice:", student.get("3rdRSS_dorm_choice"))
            print("3rd Room Choice:", student.get("3rdRSS_room_choice"))
            print("Accommodations:", student.get("Accomodations"))
            print("Personality:", student.get("Personality"))
            print("Temperature Preference:", student.get("Temperature"))
            print("Time Preference:", student.get("Time"))

        #case of student applying for dorm with tower style
        elif student.get("Accomodations") == "No, I do not require accommodations" and student.get("House_Style") == "Tower style":
            print("ID:", student.get("ID"))
            print("1st Dorm Choice:", student.get("1stRST_dorm_choice"))
            print("1st Room Choice:", student.get("1stRST_room_choice"))
            print("2nd Dorm Choice:", student.get("2ndRST_dorm_choice"))
            print("2nd Room Choice:", student.get("2ndRST_room_choice"))
            print("3rd Dorm Choice:", student.get("3rdRST_dorm_choice"))
            print("3rd Room Choice:", student.get("3rdRST_room_choice"))
            print("Accommodations:", student.get("Accomodations"))
            print("Personality:", student.get("Personality"))
            print("Temperature Preference:", student.get("Temperature"))
            print("Time Preference:", student.get("Time"))

        #case of student who requires accommodations. There is 1 suite dorm and 2 tower dorms with single rooms that have accommodations
        else:
            print("ID:", student.get("ID"))
            print("1st Dorm Choice:", student.get("1stRA_dorm_choice"))
            print("1st Room Choice: Single")
            print("2nd Dorm Choice:", student.get("2ndRA_dorm_choice"))
            print("2nd Room Choice: Single")
            print("3rd Dorm Choice:", student.get("3rdRA_dorm_choice"))
            print("3rd Room Choice: Single")
            print("Accommodations:", student.get("Accomodations"))
            print("Personality:", student.get("Personality"))
            print("Temperature Preference:", student.get("Temperature"))
            print("Time Preference:", student.get("Time"))

#print("Sorting suite dorms")
#create lists for each of the dorms that have a suite style

#print("Comet Hall data")
#CH_first_choice_students = get_students_by_dorm_choice_suite("Comet Hall", "1st")
#CH_second_choice_students = get_students_by_dorm_choice_suite("Comet Hall", "2nd")
#CH_third_choice_students = get_students_by_dorm_choice_suite("Comet Hall", "3rd")

#display_student_data(CH_first_choice_students)
#display_student_data(CH_second_choice_students)
#display_student_data(CH_third_choice_students)

#print("Moonlight hall data")
#MH_first_choice_students = get_students_by_dorm_choice_suite("Moonlight Hall", "1st")
#MH_second_choice_students = get_students_by_dorm_choice_suite("Moonlight Hall", "2nd")
#MH_third_choice_students = get_students_by_dorm_choice_suite("Moonlight Hall", "3rd")

#display_student_data(MH_first_choice_students)
#display_student_data(MH_second_choice_students)
#display_student_data(MH_third_choice_students)

#NH_first_choice_students = get_students_by_dorm_choice_suite("Nebula Hall", "1st")
#NH_second_choice_students = get_students_by_dorm_choice_suite("Nebula Hall", "2nd")
#NH_third_choice_students = get_students_by_dorm_choice_suite("Nebula Hall", "3rd")

#display_student_data(NH_first_choice_students)
#display_student_data(NH_second_choice_students)
#display_student_data(NH_third_choice_students)

#print("Sorting tower dorms")
#now create lists for each of the dorms that have a tower style
#AH_first_choice_students = get_students_by_dorm_choice_suite("Aurora Hall", "1st")
#AH_second_choice_students = get_students_by_dorm_choice_suite("Aurora Hall", "2nd")
#AH_third_choice_students = get_students_by_dorm_choice_suite("Aurora Hall", "3rd")

#display_student_data(AH_first_choice_students)
#display_student_data(AH_second_choice_students)
#display_student_data(AH_third_choice_students)

#SH_first_choice_students = get_students_by_dorm_choice_suite("Solstice Hall", "1st")
#SH_second_choice_students = get_students_by_dorm_choice_suite("Solstice Hall", "2nd")
#SH_third_choice_students = get_students_by_dorm_choice_suite("Solstice Hall", "3rd")

#display_student_data(SH_first_choice_students)
#display_student_data(SH_second_choice_students)
#display_student_data(SH_third_choice_students)

#EH_first_choice_students = get_students_by_dorm_choice_suite("Eclipse Hall", "1st")
#EH_second_choice_students = get_students_by_dorm_choice_suite("Eclipse Hall", "2nd")
#EH_third_choice_students = get_students_by_dorm_choice_suite("Eclipse Hall", "3rd")

#display_student_data(EH_first_choice_students)
#display_student_data(EH_second_choice_students)
#display_student_data(EH_third_choice_students)

#function that given a list of dictionaries, will create a list of student names that match with the given student ids in the dictionaries
def get_student_name(student_choice):

    list_student_names = []
    student_collection = get_students()

    for student in student_collection:
        for students in student_choice:

            #print(student.to_dict().get("user_id", "Unknown"))
            #print(students.get("ID"))

            #if the student id matches the form response id, that is the same student, so we add their name to the list
            if student.to_dict().get("user_id", "Unknown") == students.get("ID"):
                #print("Match found")
                list_student_names.append(student.to_dict().get("name", "Unknown"))
                break

            #else:
                #print("No Match")

    for people in list_student_names:
        print(f"list of students: {people}")

#print("Comet Hall 1st choice students:")
#get_student_name(CH_first_choice_students)
#print("Comet Hall 2nd choice students:")
#get_student_name(CH_second_choice_students)
#print("Comet Hall 3rd choice students:")
#get_student_name(CH_third_choice_students)

#print("Moonlight Hall 1st choice students:")
#get_student_name(MH_first_choice_students)
#print("Moonlight Hall 2nd choice students:")
#get_student_name(MH_second_choice_students)
#print("Moonlight Hall 3rd choice students:")
#get_student_name(MH_third_choice_students)

#print("Nebula Hall 1st choice students:")
#get_student_name(NH_first_choice_students)
#print("Nebula Hall 2nd choice students:")
#get_student_name(NH_second_choice_students)
#print("Nebula Hall 3rd choice students:")
#get_student_name(NH_third_choice_students)

#print("Aurora Hall 1st choice students:")
#get_student_name(AH_first_choice_students)
#print("Aurora Hall 2nd choice students:")
#get_student_name(AH_second_choice_students)
#print("Aurora Hall 3rd choice students:")
#get_student_name(AH_third_choice_students)

#print("Solstice Hall 1st choice students:")
#get_student_name(SH_first_choice_students)
#print("Solstice Hall 2nd choice students:")
#get_student_name(SH_second_choice_students)
#print("Solstice Hall 3rd choice students:")
#get_student_name(SH_third_choice_students)

#print("Eclipse Hall 1st choice students:")
#get_student_name(EH_first_choice_students)
#print("Eclipse Hall 2nd choice students:")
#get_student_name(EH_second_choice_students)
#print("Eclipse Hall 3rd choice students:")
#get_student_name(EH_third_choice_students)

