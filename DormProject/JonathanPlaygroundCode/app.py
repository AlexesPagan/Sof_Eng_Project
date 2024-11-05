from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import firebase_admin
from firebase_admin import auth, credentials, firestore  # Import Firestore

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key'  # Needed for session management

# Initialize Firebase Admin with your service account key
cred = credentials.Certificate(r"C:\Users\fasan\Desktop\SuiteDreams\databasebuilds-firebase-adminsdk-arl8u-c0af0513df.json")
firebase_admin.initialize_app(cred)

db = firestore.client()  # Initialize Firestore client

# Middleware function to verify the Firebase token
def verify_firebase_token():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        id_token = auth_header.split(' ')[1]  # Extract token
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token  # Decoded token includes user information (e.g., uid)
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None
    return None 

@app.route('/protected-route', methods=['POST'])
def protected_route():
    user = verify_firebase_token()
    if user:
        session['user_id'] = user['uid']
        session['email'] = user['email']

        # Query Firestore for user data
        user_data = db.collection('users').document(user['uid']).get()  # Use the initialized db object
        if user_data.exists:
            session['name'] = user_data.to_dict().get('name', user['email'])  # Default to email if no name exists
        else:
            session['name'] = user['email']  # Fallback if no user data is found

        return jsonify({"message": f"Hello, {session['name']}!", "name": session['name']}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/')
def login():
    return render_template('T3_T1_LoginUI_copy.html')

@app.route('/T4_StudentHomepage')
def student_homepage():
    if 'email' in session:
        email = session['email']  # Get email from session
        name = session.get('name', email)  # Get name from session, default to email
        return render_template('T4_StudentHomepage.html', name=name)  # Pass name to the template
    else:
        return redirect('/login')  # Redirect to login if not logged in
    
@app.route('/logout', methods=['POST'])  # Ensure 'POST' is included here
def logout():
    session.pop('user_id', None)  # Clear the session
    return redirect(url_for('login'))  # Redirect to login after logout

if __name__ == '__main__':
    app.run(debug=True)