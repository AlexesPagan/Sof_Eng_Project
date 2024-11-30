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



#import firebase_admin
#from firebase_admin import credentials, firestore, auth
#import re

# Path to the service account JSON file
#cred = credentials.Certificate(r"C:\Users\Kyren\OneDrive\Desktop\Suite_Dreams_SK\databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")  # Update the path
#firebase_admin.initialize_app(cred)

# Initialize Firestore

#db = firestore.client()


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


#function that will either add or remove a specified student from a dorm room.
#all excluded print statements are just used for testing purposes
def add_or_remove_student(dorm_name, room_number, student_id, task, db):

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

                if task == "add":

                    print("adding student")

                    #add the specified student id to the student list and then call firebase to update the data of the specified document id
                    students.append({"ID": student_id})
                    db.collection('dorms').document(dorm_id).update({'rooms': dorm_data['rooms']})

                elif task == "remove":
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

#add_or_remove_student("Test Dorm", "Rm06", "H777777777", "add")

#add_or_remove_student("Test Dorm", "Rm06", "H777777777", "remove")

#------------------------------------------------------------------------------------


