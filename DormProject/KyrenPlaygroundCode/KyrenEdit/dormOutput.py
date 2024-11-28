#from firebase_admin import credentials, auth, firestore, initialize_app

# Initialize Firebase Admin SDK
#cred = credentials.Certificate(r"C:\Users\Kyren\OneDrive\Desktop\Suite_Dreams_SK\databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")
#initialize_app(cred)
#db = firestore.client()

#targetStudent = 'H400000000' #Testing the value for the Tryhard


# if a student has roommates, we can list them here. 
def countRoommates(logStu, studentsID):
    roommates = []
    for student in studentsID:
        if student == logStu:
            continue
        else:
            roommates.append(student)
    return roommates


# This finds a specific student in a room (This is the cross-check)
def findStudent(dormitory, ID_num):
    for dormName in dormitory:                                                      # access the dorm names from the dormitory library
        roomNums = dormitory[dormName]                                              # unpacks the occupied rooms from the dormitory library
        for room in roomNums:                                                       # access the individual room numbers 
            students_ID = roomNums[room]                                            # unpacks the student IDs from the occupied rooms
            for stu_ID in students_ID:                                              # for each ID in th student IDs previously unpacked...
                if stu_ID == ID_num:                                                # check to see if the ID matches the one we're looking for
                    if len(students_ID) > 1:
                        roommates = countRoommates(stu_ID, students_ID)
                        return room, dormName, roommates                            # when a pair is found, end the for loop, return the location values, and the roommates
                    else:
                        return room, dormName, 'You do not have any roommates.'     # when a pair is found, end the for loop and return the location values. 
    return 'Not found. Have you submitted the dorm application?', 'N/A', 'N/A'      # if the pair is not found, indicate so


# This creates the initial dictionary of all the dorms, occupied rooms, and the students who reside there
def createDormitory(db):
    dorms_ref = db.collection('dorms') # Accessing the dorm collection
    dorms = dorms_ref.stream() # Get all dorm documents || .stream() gets the data in real time. 
    student_ref = db.collection('students')
    students = student_ref.stream()
    dormitory = {}
    
    for student_stuff in students:
        student_data = student_stuff.to_dict()      # this gets the student data from the database and puts it into a dictionary

    for dorm_stuff in dorms:
        dorm_data = dorm_stuff.to_dict()            # this gets the dorm data from the database and puts it into a dictionary
        dorm_name = dorm_data.get('name')           # Getting the dormitory's name ("Comet Hall")
        dormitory[dorm_name] = {}                   # We create a base dictionary that has the dormitory names as the initial key.
        rooms = {}                                  # initialize this here so it refreshes every iteration.
        for room in dorm_data['rooms']:             # The dorm_data is in a dictionary that has each dormitory within. The key for these dorms is 'room'
            dorm_rooms = room.get('room_number')    # the room numbers for the room we're on in the for loop
            students = []                           # this refreshes with every new room 
            if room.get('students') != []:          # If a student occupies the room, otherwise it isn't loaded
                for stu in room['students']:        # for every student in the room
                    students.append(stu.get("ID"))  # put their student ID into the room
                rooms[dorm_rooms] = students        # put this list of students into their respective room        
            dormitory[dorm_name] = rooms            # add this room and it's students into the dorm
    return dormitory



# maybe say that if only one student in a room, they're in a single. for the number of items in the dictionary, label the room. 

# TESTING CODE #

#dormitory = createDormitory()
#print(dormitory)

#stuRoom, stuBuilding, stuRoommates = findStudent(dormitory, targetStudent)
#print (stuBuilding, stuRoom, stuRoommates) 