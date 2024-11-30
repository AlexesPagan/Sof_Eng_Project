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


// Actual button clicks, using the general function created

// Actual button clicks, using the general function created
document.getElementById('dormDetailsButton').addEventListener('click',function(){
  toggleButton('dorm-details')
});

document.getElementById('Dorm_1_Details_Button').addEventListener('click', function(){
  toggleButton('DD-Dorm-1-Page')
});

document.getElementById('dormApplicationButton').addEventListener('click',function(){
  toggleButton('dorm-application')
});

document.getElementById('overviewButton').addEventListener('click', function(){
  toggleButton('overview-page')
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

document.getElementById('SuiteRoomButton').addEventListener('click',function(){
  toggleButton('SuiteRoomDetails')
});


