from firebase_admin import credentials, auth, firestore, initialize_app

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\fasan\Desktop\SuiteDreams\serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

dorms_ref = db.collection('dorms') # Accessing the dorm collection
dorms = dorms_ref.stream() # Get all dorm documents || .stream() gets the data in real time. 
student_ref = db.collection('students')
students = student_ref.stream()


dormitory = {}
targetStudent = 'H400000000' #Testing the value for the Tryhard
stuRoom = ''
stuBuilding = ''
type_Room = ''

#def roomType(dormitory):

def findStudent(dormitory, ID_num):

    for dormName in dormitory:            # access the dormitory names
        roomNum = dormitory[dormName]     # keep track of the rooms in the dorm
        for room in roomNum:              # access the individual rooms in the dorm
            students_ID = roomNum[room]   # keep track of the student IDs in the individual rooms 
            for stu_ID in students_ID:    # access the string form of the student IDs in the rooms
                if stu_ID == ID_num:      # check to see if the pair is valid , if not keep trying.
                    return room, dormName # when a pair is found, end the for loop and return the location values. 
    return 'Not found', 'Not found'


# This creates the initial dictionary of all the dorms, occupied rooms, and the students who reside there
for student_stuff in students:
    student_data = student_stuff.to_dict()

for dorm_stuff in dorms:
    dorm_data = dorm_stuff.to_dict()
    dorm_name = dorm_data.get('name') # Getting the dormitory's name ("Comet Hall")

    dormitory[dorm_name] = {} # We create a base dictionary that has the dormitory names as the initial key.
    rooms = {} #initialize this here so it refreshes every iteration.

    for room in dorm_data['rooms']: # The dorm_data is in a dictionary that has each dormitory within. The key for these dorms is 'room'
        dorm_rooms = room.get('room_number')  # the room numbers for the room we're on in the for loop
        if room.get('students') != []: # If a student occupies the room, otherwise it isn't loaded.
            for stu in room['students']: # for every student in the room
                students = []
                students.append(stu.get("ID")) # put their student ID into the room
            rooms[dorm_rooms] = students # put this list of students into their respective room
        dormitory[dorm_name] = rooms # add this room and it's students into the dorm





stuRoom, stuBuilding = findStudent(dormitory, targetStudent)
print (stuBuilding, stuRoom)

#print(dormitory) # testing
