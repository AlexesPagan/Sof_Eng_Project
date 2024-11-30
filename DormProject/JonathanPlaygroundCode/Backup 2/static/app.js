// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAqgAgCfYGQSkBgYmD1zD9gDI3EmY8rFPA",
    authDomain: "databasebuilds.firebaseapp.com",
    projectId: "databasebuilds",
    storageBucket: "databasebuilds.firebasestorage.app",
    messagingSenderId: "126520572285",
    appId: "1:126520572285:web:4584fcb8b5291722557414",
    measurementId: "G-99VBEB1WJQ"
  };

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('inputEmail').value;
    const password = document.getElementById('inputPassword').value;
    const errorMessage = document.getElementById('errorMessage');

    try {
        // Attempt to sign in
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        const user = userCredential.user;

        // Get the ID token
        const idToken = await user.getIdToken();

        // Send the ID token to your Flask backend
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idToken: idToken }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                errorMessage.textContent = 'Unknown user role';
            }
        } else {
            const errorData = await response.json();
            errorMessage.textContent = errorData.error || 'Server error. Please try again.';
        }
    } catch (error) {
        errorMessage.textContent = 'Incorrect email or password';
        console.error('Error:', error);
    }
});