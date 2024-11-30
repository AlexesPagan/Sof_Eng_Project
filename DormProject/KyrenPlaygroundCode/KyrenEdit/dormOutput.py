#from firebase_admin import credentials, auth, firestore, initialize_app

#cred = credentials.Certificate(r"C:\Users\Kyren\OneDrive\Desktop\Suite_Dreams_SK\databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")
#initialize_app(cred)
#db = firestore.client()


# if a student has roommates, we can list them here. 
def countRoommates(logStu, studentsID):
    roommates = []
    for student in studentsID:
        if student == logStu:
            continue
        else:
            roommates.append(student)
    return roommates


#particularly for admin, literally just locating if a student exists. 
def findStudentAdmin(dormitory, ID_num, roomNum, dorm, action):
    perm_capacity = 0
    curr_capacity = 0
    for dormName in dormitory:                                                                             # access the dorm names from the dormitory library
        roomNums = dormitory[dormName]                                                                     # unpacks the occupied rooms from the dormitory library
        for room in roomNums:                                                                              # access the individual room numbers 
            students_ID = roomNums[room]                                                                   # unpacks the student IDs from the occupied rooms
            for stu_ID in students_ID:                                                                     # for each ID in th student IDs previously unpacked...
                if (stu_ID == ID_num and room == roomNum and dormName == dorm and action == 'remove'):     # check to see if the ID matches the one we're looking for and the action is remove
                    return True                                                                            # greenlight to move to next step
                elif (stu_ID == ID_num and action == 'add'):                                               # if the student exists and the action was add...
                    return False                                                                           # red light, they need to remove the student first
    if (action == 'add'):
        return True
    return False


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
    capacity = {}
    
    for student_stuff in students:
        student_data = student_stuff.to_dict()          # this gets the student data from the database and puts it into a dictionary

    for dorm_stuff in dorms:
        dorm_data = dorm_stuff.to_dict()                # this gets the dorm data from the database and puts it into a dictionary
        dorm_name = dorm_data.get('name')               # Getting the dormitory's name ("Comet Hall")
        dormitory[dorm_name] = {}                       # We create a base dictionary that has the dormitory names as the initial key.
        rooms = {}                                      # initialize this here so it refreshes every iteration.
        perm_capacity = dorm_data.get('capacity')       # this gets the initial capacity of the dorms so we can figure out how many slots are left. 
        capacity[dorm_name] = perm_capacity             # this keeps track of the capacity in each dorm.
        for room in dorm_data['rooms']:                 # The dorm_data is in a dictionary that has each dormitory within. The key for these dorms is 'room'
            dorm_rooms = room.get('room_number')        # the room numbers for the room we're on in the for loop
            students = []                               # this refreshes with every new room 
            if room.get('students') != []:              # If a student occupies the room, otherwise it isn't loaded
                temp = capacity[dorm_name]              # this reduces the capacity in a dorm room
                temp -= len(room.get('students'))       
                capacity[dorm_name] = temp
                for stu in room['students']:            # for every student in the room
                    students.append(stu.get("ID"))      # put their student ID into the room
                rooms[dorm_rooms] = students            # put this list of students into their respective room        
            dormitory[dorm_name] = rooms                # add this room and it's students into the dorm
    return dormitory

def findCapicity(db):
    dorms_ref = db.collection('dorms') # Accessing the dorm collection
    dorms = dorms_ref.stream() # Get all dorm documents || .stream() gets the data in real time. 

    capacity = {}
    
    for dorm_stuff in dorms:
        dorm_data = dorm_stuff.to_dict()                # this gets the dorm data from the database and puts it into a dictionary
        dorm_name = dorm_data.get('name')               # Getting the dormitory's name ("Comet Hall")

        perm_capacity = dorm_data.get('capacity')       # this gets the initial capacity of the dorms so we can figure out how many slots are left. 
        capacity[dorm_name] = perm_capacity             # this keeps track of the capacity in each dorm.
        for room in dorm_data['rooms']:                 # The dorm_data is in a dictionary that has each dormitory within. The key for these dorms is 'room'
            if room.get('students') != []:
                capacity[dorm_name] -= len(room.get('students'))

    return capacity


def applicationNum(db):
    forms_ref = db.collection('form_responses')
    curr_forms = forms_ref.stream()
    num_forms = 0
    for forms in curr_forms:
        num_forms += 1
    return(num_forms)


# TESTING CODE #

#dormitory = createDormitory(db)
#print(dormitory)

#stuRoom, stuBuilding, stuRoommates = findStudent(dormitory, 'H400000000')
#print (stuBuilding, stuRoom, stuRoommates) 

#number = applicationNum(db)
#print(number)

#print(findStudentAdmin(dormitory, 'H998877665', 'Rm06', 'Comet Hall', 'add'))
#print(findStudentAdmin(dormitory, 'H998877666', 'Rm06', 'Comet Hall', 'add'))
#print(findStudentAdmin(dormitory, 'H998877665', 'Rm06', 'Comet Hall', 'remove'))
#print(findStudentAdmin(dormitory, 'H998877666', 'Rm06', 'Comet Hall', 'remove'))