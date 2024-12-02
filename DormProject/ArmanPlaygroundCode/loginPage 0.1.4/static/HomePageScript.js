// HomePageScript.js

// Wait for the DOM to fully load before executing the script
document.addEventListener('DOMContentLoaded', function() {
  // Store a reference to the currently active section
  let activeSection = document.getElementById('overview-page'); 
  
  // Function to hide all sections
  function hideAllSections() {
      const sections = document.querySelectorAll('.content-section');
      sections.forEach(section => {
          section.style.display = 'none';
      });
  }

  // Function to toggle the visibility of a section
  function toggleSection(sectionId) {
      const targetSection = document.getElementById(sectionId);
      if (!targetSection) {
          console.warn(`Section with ID '${sectionId}' not found.`);
          return;
      }

      if (activeSection === targetSection) {
          // If the target section is already active, hide it
          targetSection.style.display = 'none';
          activeSection = null;
          removeActiveClassFromAllButtons();
      } else {
          // Hide the currently active section
          if (activeSection) {
              activeSection.style.display = 'none';
          }

          // Show the target section
          targetSection.style.display = 'block';
          activeSection = targetSection;

          // Update active button styling
          setActiveButton(sectionId);
      }
  }

  // Function to initialize the visibility of sections
  function initializeSections() {
      // Select all sections (add a common class 'content-section' to each in HTML)
      const sections = document.querySelectorAll('.content-section');
      
      sections.forEach(section => {
          if (section.id === 'overview-page') {
              section.style.display = 'block'; // Show the overview page by default
              activeSection = section;
          } else {
              section.style.display = 'none'; // Hide other sections
          }
      });
  }

  // Map button IDs to their corresponding section IDs
  const buttonSectionMap = {
      'overviewButton': 'overview-page',
      'dormApplicationButton': 'dorm-application',
      'dormDetailsButton': 'dorm-details',
      'helpButton': 'help-page',
      'Dorm_1_Details_Button': 'DD-Dorm-1-Page',
      // Add more mappings if there are additional buttons and sections
      'SingleRoomButton': 'SingleRoomDetails',
      'DoubleRoomButton': 'DoubleRoomDetails',
      'SuiteRoomButton': 'SuiteRoomDetails'
  };

  // Function to set up event listeners for all navigation buttons
  function setupEventListeners() {
      for (const [buttonId, sectionId] of Object.entries(buttonSectionMap)) {
          const button = document.getElementById(buttonId);
          const section = document.getElementById(sectionId);
          
          if (!button) {
              console.warn(`Button with ID '${buttonId}' not found.`);
              continue;
          }
          
          if (!section) {
              console.warn(`Section with ID '${sectionId}' not found.`);
              continue;
          }

          button.addEventListener('click', function(event) {
              event.preventDefault(); // Prevent default behavior if the button is a link
              toggleSection(sectionId);
          });
      }
  }

  // Function to set the active class on the corresponding button
  function setActiveButton(sectionId) {
      removeActiveClassFromAllButtons();
      const activeButton = document.querySelector(`.nav-link[data-section="${sectionId}"]`);
      if (activeButton) {
          activeButton.classList.add('active');
      }
  }

  // Function to remove the active class from all buttons
  function removeActiveClassFromAllButtons() {
      const buttons = document.querySelectorAll('.nav-link');
      buttons.forEach(button => {
          button.classList.remove('active');
      });
  }

  // Initialize sections on page load
  initializeSections();

  // Set up event listeners for navigation buttons
  setupEventListeners();
});