
from firebase_admin import credentials, auth, firestore, initialize_app


# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\fasan\Desktop\SuiteDreams\serviceAccountKey.json")

initialize_app(cred)

db = firestore.client()


# Accessing the dorm collection
dorms_ref = db.collection('dorms')

# Get all dorm documents
dorms = dorms_ref.stream()

student_ref = db.collection('students')

studentss = student_ref.stream()

for student_stuff in studentss:
    student_data = student_stuff.to_dict()

    print(student_data)
    
# Iterate through each dorm document
for dorm_stuff in dorms:

    dorm_data = dorm_stuff.to_dict()  # Convert the document to a dictionary
   # Access rooms in the dorm
    rooms = dorm_data.get('rooms', [])

    for room in rooms:

        
        # Access students in each room
        students = room.get('students', [])

        if students:
            print(f"Students in Room {room['room_number']}:")

            for student in students:
                print(f"{student}")

        else:
            print(f"No students assigned to Room {room['room_number']}.")
    