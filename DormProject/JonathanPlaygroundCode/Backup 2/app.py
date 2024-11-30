from flask import Flask, request, jsonify, session, redirect,render_template, url_for, g # type: ignore
# Import necessary modules from Flask: 
# - Flask: for initializing the app
# - request: to handle incoming HTTP requests
# - jsonify: to return JSON responses
# - session: to manage user sessions
# - redirect: to redirect users to different routes
# - render_template: to render HTML templates
# - url_for: to generate URLs for routes
# - g: for storing request-specific data (like start time for logging)



from firebase_admin import credentials, auth, firestore, initialize_app # type: ignore

# Import Firebase Admin SDK components:
# - credentials: to authenticate with Firebase using a service account
# - auth: for handling Firebase authentication
# - firestore: to interact with Firestore database
# - initialize_app: to initialize the Firebase app


from functools import wraps
# Import wraps from functools to handle route decorators (like login_required)

import os
# Import os to handle file paths and environment variables

import logging
# Import logging to log request and response information

import time  # Import time for measuring request duration

import re


# Initialize a Flask app, setting the static file directory to 'static'
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = os.urandom(24)  # Set a secret key for sessions
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# the file is in the same directory as the script
#service_account_path = os.path.join(current_dir,'config','serviceAccountKey.json')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\fasan\Desktop\SuiteDreams\serviceAccountkey.json")

initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Set up logging configuration
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#Middleware for logging requests and responses
@app.before_request
def log_request_info():
    g.start_time = time.time()  # Record the start time
    logging.info(f"Request: {request.method} {request.url} User ID: {session.get('user_id')} Role: {session.get('role')}")

@app.after_request
def log_response_info(response):
    duration = time.time() - g.start_time  # Calculate the duration
    logging.info(f"Response: {response.status} Duration: {duration:.2f}s")
    return response


# Middleware to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=['POST'])
def login():
    id_token = request.json['idToken']
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']# Extract the user ID (uid) from the decoded token
        
        # Fetch user data from Firestore
        user_doc = db.collection('admins').document(uid).get()
        if not user_doc.exists:
            user_doc = db.collection('students').document(uid).get()
            if not user_doc.exists:
                return jsonify({'error': 'User not found in database'}), 404
        
        user_data = user_doc.to_dict()
        name = user_data.get('name')  # Get the name
        role = user_data.get('role')# Get the user's role (e.g., 'admin', 'student') from the user data
        
        if role not in ['admin', 'student']:
            return jsonify({'error': 'Invalid user role'}), 403
        
        # Set session data
        session['user_id'] = uid
        session['role'] = role
        session['name'] = name  # Store name in session

        
        # Return the role and redirect URL
        if role == 'admin':
            return jsonify({'role': role, 'redirect': url_for('admin_page')}), 200
        else:
            return jsonify({'role': role, 'redirect': url_for('student_page')}), 200
        
    except auth.InvalidIdTokenError:
        return jsonify({'error': 'Invalid ID token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
@login_required
def admin_page():
    if session['role'] != 'admin':# If the logged-in user is not an admin, redirect them to the index (login) page
        return redirect(url_for('index'))
    return render_template('T5_AdminHomepage.html')
    

@app.route('/student')
@login_required
def student_page():
    if session['role'] != 'student':# If the logged-in user is not a student, redirect them to the index (login) page
        return redirect(url_for('index'))
    return render_template('T4_StudentHomepage.html')

@app.route('/logout', methods=['POST']) # CHANGED THIS TO A POST METHOD BECAUSE IT IS A LOGOUT
def logout():
    session.clear()
    return redirect(url_for('index'))# Clear the session to log the user out

@app.route('/')
def index():
    return render_template('T1_LoginUI.html')

if __name__ == '__main__':
    app.run(debug=True)# Run the Flask app in debug mode

################################################################################################################################################
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