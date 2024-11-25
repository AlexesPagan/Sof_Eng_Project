# Kyren - This code has been taken from Alexes' playground code and altered to better fit the frontend's needs.


def get_responses(): # function to get all responses from the form_responses collection
    return db.collection('form_responses').stream()

def get_students():
    students_ref = db.collection('students') #sets a reference to the database
    students = students_ref.stream() #use stream() in order to get all data from the database reference
    student_list = []

    for student in students: #iterate through the entire database
        student_list.append(student)
    return student_list

def parse_response_data():
    student_example = get_students() # get all data from student collection
    student_id_test = [student.to_dict().get('user_id', 'Unknown') for student in student_example] # creates a dictionary of the student data containing only their student id
    #print(student_id_test)
    response_example = get_responses() # get all data from the form_responses collection
    response_data = [(response.to_dict().get("ID", "Unknown"), response.reference) for response in response_example] # create a list of tuples which includes the id from the form response and the firestore document reference to that response
    response_ids = [response[0] for response in response_data] # create a list taking only the id data from response_data
    #print(response_ids)
    StudentID = ''

    for response_id, reference in response_data: #iterate through each tuple in the list of tuples
        valid_data = False #variable to signify a valid id comparison
        for id in student_id_test: #iterate through each student id
            #print(f"comparing {response_id} with {id}")
            if response_id != id: #if the id specified in the form does not match the student id, it is an invalid id
                continue
            else: #if the id specified in the form does match, it is a valid id. Break to exit this for loop
                valid_data = True
                StudentID = id
                print(f"valid id: {valid_data}")
                break
    return StudentID