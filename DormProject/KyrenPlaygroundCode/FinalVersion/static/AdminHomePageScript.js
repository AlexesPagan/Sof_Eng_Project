let activeElement = document.getElementById('overview-page'); 
let lastActiveItem = null; // To store the last active item
function setActive(element) {
  // Remove active style from all items
  const items = document.querySelectorAll('.dropdown-item');
  items.forEach(item => {
    item.style.backgroundColor = '';
    item.style.color = '#1a2f4a'; // Reset color
  });
  // Set active style for the clicked item
  element.style.backgroundColor = '#d2c6d3'; // Change to your desired color
  lastActiveItem = element; // Store the last active item
}

// Remove highlight when clicking outside the dropdown
document.addEventListener('click', function(event) {
  const dropdownMenu = document.querySelector('.dropdown-menu');
    // Check if the click was outside the dropdown
    if (!dropdownMenu.contains(event.target) && lastActiveItem) {
      lastActiveItem.style.backgroundColor = ''; // Reset background color
      lastActiveItem.style.color = '#1a2f4a'; // Reset text color
      lastActiveItem = null; // Clear the last active item
    }
});

// THIS IS TO GET THE DORM DETAILS PAGE TO APPEAR ON CLICK
// THIS IS NOW REUSABLE, JUST CALL THIS FUNCTION AFTER AN EVENTLISTENER
function toggleButton(element){
  const elementID = document.getElementById(element);
  console.log(activeElement);

  // If another element is already active, hide it
  if (activeElement && activeElement !== elementID) {
      activeElement.style.visibility = 'hidden'; // Hide the previously active element
  }

  // If the clicked element is hidden, show it
  if (elementID.style.visibility === 'hidden' || elementID.style.visibility === '') {
    elementID.style.visibility = 'visible';
    activeElement = elementID; // Set this element as the active one
  } 
}


// In the admin page specifically... (I (Kyren) got this code from Jonathan)

// Define sendData function
function sendData(ID, dorm, room, choice) {
  fetch('/validateStu', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ID: ID,
      dorm: dorm,
      room: room,
      choice: choice.toLowerCase()
    })
  })
  .then(response => response.json())
  .then(result => {
    const messageElement = document.getElementById('studentMessage');  // Reference the modal message element
    if (result == true) {
      console.log('Student found:', result);
      messageElement.textContent = `Student ${ID} found in ${dorm} ${room}. Action: ${choice}`;
      showModal();
    } else if (result == false && choice == 'add') {
      console.log('Student found:', result);
      messageElement.textContent = `Student ${ID} found in another dorm. Please remove them and then try again`;
      showModal();
    } else {
      console.log('Student found:', result);
      messageElement.textContent = `Student ${ID} not found in ${dorm} ${room}. Please try again.`;
      showModal();
    }
  })
  .catch(error => {
    console.error('Error:', error);
    const messageElement = document.getElementById('studentMessage');
    messageElement.textContent = 'An error occurred while processing your request. Please try again later.';
    showModal();
  });
}

// Function to show the modal
function showModal() {
const modal = new bootstrap.Modal(document.getElementById('studentModal'));
modal.show();
}



// Actual button clicks, using the general function created


document.getElementById('addRemoveButton').addEventListener('click',function(){
    //console.log("in function!")
    stuID = document.getElementById("StuIDInput").value; // You use the .value key to get the value entered by the user in the text element
    building = document.getElementById("DormHallInput").value;
    room = document.getElementById("RoomNumInput").value;
    choice = (document.getElementById("AddDeleteInput")).value;
    //console.log(stuID, building, room, choice)
    sendData(stuID, building, room, choice)
  })
  
document.getElementById('dormDetailsButton').addEventListener('click',function(){
  toggleButton('dorm-details')
});

document.getElementById('Dorm_1_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('Dorm_2_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('Dorm_3_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('Dorm_4_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('Dorm_5_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('Dorm_6_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-Page')
});

document.getElementById('overviewButton').addEventListener('click', function(){
  toggleButton('overview-page')
})

document.getElementById('studentResponsesButton').addEventListener('click', function(){
  toggleButton('stu-resp-page')
})

document.getElementById('helpButton').addEventListener('click', function(){
  toggleButton('help-page')
})

document.getElementById('SingleRoomButton').addEventListener('click', function() {
  toggleButton('SingleRoomDetails');
});

document.getElementById('DoubleRoomButton').addEventListener('click',function(){
  toggleButton('DoubleRoomDetails')
});

document.getElementById('TripleRoomButton').addEventListener('click',function(){
  toggleButton('TripleRoomDetails')
});

document.getElementById('QuadRoomButton').addEventListener('click',function(){
  toggleButton('QuadRoomDetails')
});

document.getElementById('QuintRoomButton').addEventListener('click',function(){
  toggleButton('QuintRoomDetails')
});



