const firebaseConfig = {

    apiKey: "AIzaSyBFq5VEM92Ean7E2njT-CNlyhUZkS7SqN8",
  
    authDomain: "suite-dreams-ddfd4.firebaseapp.com",
  
    projectId: "suite-dreams-ddfd4",
  
    storageBucket: "suite-dreams-ddfd4.appspot.com",
  
    messagingSenderId: "532007287219",
  
    appId: "1:532007287219:web:36219a1ea7cad730b373c6",
  
    measurementId: "G-LJQS6H1D51"
  
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