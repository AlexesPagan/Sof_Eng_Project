# REVISION HISTORY
# Parsa     10/20/2024  Added the Admin class, refined the user role logic, and improved input validation for a streamlined and error-free user experience.
# Parsa     10/20/2024  Implemented synchronization between Firestore and Firebase Authentication to ensure that each user's Firestore document ID is used as their Firebase Authentication UID upon creation.
#



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
new_user = create_user()

# Role-specific actions
if isinstance(new_user, Admin):
    new_user.view_student_info('S123')
    new_user.change_room_assignment('S123', 'Room 102')
elif isinstance(new_user, Student):
    update_data = {'year': 'Junior', 'preferences': ['quiet', 'library']}
    update_user_info(new_user.user_id, update_data)

get_users()
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