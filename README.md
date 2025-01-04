# Suite Dreams

**Suite Dreams** is an automated dorm allocation application designed to streamline the process of assigning dorm rooms and roommates to college students. By utilizing a sophisticated matching algorithm, the application ensures that students are matched with compatible roommates and assigned to preferred dorm rooms, enhancing student satisfaction and reducing administrative workload.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Team Members](#team-members)

---

## Features

- **User Authentication**: Secure login system using Firebase Authentication.
- **Student Application Form**: Allows students to submit housing preferences and roommate requests.
- **Matching Algorithm**: Calculates compatibility scores based on student preferences.
- **Room Assignment**: Automatically assigns students to rooms and roommates.
- **Admin Dashboard**: Enables administrators to monitor occupancy and manage room assignments.
- **Real-Time Updates**: Keeps user interfaces synchronized with the database changes.
- **Accessibility Support**: Accommodates students with specific accessibility needs.

---

## Architecture

Suite Dreams follows the **Model-View-Controller (MVC)** architectural pattern:

- **Model**: Handles data management using Firebase/Firestore. Includes data models and the `data.py` module for database interactions.
- **View**: Consists of the user interface built with HTML, CSS, JavaScript, and Bootstrap. Renders templates and captures user input.
- **Controller**: Implements application logic using Flask. Processes user requests, interacts with the model, and returns responses.

The matching algorithm employs a **Pipe and Filter** architecture, processing student applications through sequential stages:

1. **Data Collection**: Retrieves student applications from the database.
2. **Data Validation**: Ensures completeness and correctness of applications.
3. **Grouping Students**: Forms roommate groups based on preferences.
4. **Compatibility Scoring**: Calculates scores using weighted criteria.
5. **Room Assignment**: Assigns students to rooms based on compatibility and availability.
6. **Notification**: Communicates assignment results to students.

---

## Technologies Used

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Bootstrap for responsive design
- **Backend**:
  - Python
  - Flask framework
- **Database**:
  - Firebase Firestore for real-time data storage
  - Firebase Authentication for secure user login
- **External Services**:
  - Google Forms and Sheets for data collection
- **Version Control**:
  - Git and GitHub for code collaboration

---

## Installation

### Prerequisites

- Python 3.x installed on your system
- Firebase account with Firestore and Authentication set up
- Google Cloud credentials for Firebase Admin SDK

### Steps

1. **Clone the Repository**

2. **Create a Virtual Environment**

3. **Set Up Firebase Credentials**

   - Place your `serviceAccountKey.json` file (Firebase Admin SDK key) in the project root directory.
   - Ensure your Firebase project is properly configured with Firestore and Authentication.

4. **Configure Environment Variables**

5. **Initialize the Database**

   - Run any necessary scripts to set up your Firestore database structure.

6. **Run the Application**

---

## Usage

### For Students

1. **Logining In**

   - Visit the login page and sign with your school email and password.

2. **Fill Out the Application Form**

   - Complete the housing application form, specifying your dorm preferences and roommate requests.

3. **Submit Preferences**

   - Provide information on your lifestyle preferences for compatibility scoring.

4. **Receive Assignment**

   - After processing, view your dorm and roommate assignment in your dashboard.

### For Administrators

1. **Login to Admin Dashboard**

   - Access the admin panel using your administrator credentials.

2. **Monitor Applications**

   - View submitted applications and track occupancy rates.

3. **Manage Assignments**

   - Override or adjust room assignments as needed.

4. **Generate Reports**

   - Export data and generate reports on housing assignments.

---

## Contributing

We welcome contributions from the community. To contribute:

1. **Fork the Repository**

   - Click the "Fork" button at the top right of the repository page.

2. **Commit Your Changes**

   ```bash
   git commit -m "Add your message here"
   ```

3. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeature
   ```

4. **Submit a Pull Request**

   - Go to the original repository and create a pull request from your fork.

---

### Guidelines

- Follow the existing code style and structure.
- Write clear commit messages.
- Include documentation for new features.
- Ensure all tests pass before submitting.

---

## Team Members

- **Kyren Stephenson**: Frontend Developer, UI/UX Designer
- **Jonathan Fasano**: Documentation Coordinator, API Integration Specialist, Frontend Developer
- **Alexes Pagan**: Database Manager, Firebase Expert
- **John Doyle**: QA Tester, Quality Assurance Lead
- **Parsa Jafaripour**: Project Manager, Algorithm Developer, Matching Logic Specialist

---

## Contact

For any inquiries or support, please contact us at:

- **Email**: parsajafaripour@gmail.com
