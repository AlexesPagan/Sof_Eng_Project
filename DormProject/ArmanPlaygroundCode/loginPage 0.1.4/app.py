from flask import Flask, request, jsonify, session, redirect,render_template, url_for, g
# Import necessary modules from Flask: 
# - Flask: for initializing the app
# - request: to handle incoming HTTP requests
# - jsonify: to return JSON responses
# - session: to manage user sessions
# - redirect: to redirect users to different routes
# - render_template: to render HTML templates
# - url_for: to generate URLs for routes
# - g: for storing request-specific data (like start time for logging)



from firebase_admin import credentials, auth, firestore, initialize_app

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




# Initialize a Flask app, setting the static file directory to 'static'
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = os.urandom(24)  # Set a secret key for sessions
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# the file is in the same directory as the script
service_account_path = os.path.join(current_dir,'config','serviceAccountKey.json')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_path)

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


# Function to fetch dorm details and students
def get_dorm_info():
    dorms_ref = db.collection('dorms')  # Reference to 'dorms' collection
    dorms = dorms_ref.stream()  # Fetch all dorm documents

    dorm_info = []  # This will store the dorm data including students
    for dorm in dorms:
        dorm_data = dorm.to_dict()
        dorm_name = dorm_data.get('name', 'Unknown Dorm')
        rooms = dorm_data.get('rooms', [])
        
        for room in rooms:
            students = room.get('students', [])
            room_number = room.get('room_number', 'Unknown Room')
            is_occupied = room.get('is_occupied', False)

            dorm_info.append({
                'dorm_name': dorm_name,
                'room_number': room_number,
                'students': students,  # List of students in the room
                'is_occupied': is_occupied
            })

    return dorm_info


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
    dorm_info = get_dorm_info()  # Get dorm data including students
    return render_template('T5_AdminHomepage.html')
    

@app.route('/student')
@login_required
def student_page():
    if session['role'] != 'student':# If the logged-in user is not a student, redirect them to the index (login) page
        return redirect(url_for('index'))
    return render_template('T4_StudentHomepage.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))# Clear the session to log the user out

@app.route('/')
def index():
    return render_template('T1_LoginUI.html')

if __name__ == '__main__':
    app.run(debug=True)# Run the Flask app in debug mode