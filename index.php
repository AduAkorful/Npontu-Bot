<?php
$botName = "NpontuChat";
$backendUrl = getenv("BACKEND_API_URL") ?: "https://npontu-bot-production.up.railway.app";
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><?php echo $botName; ?> - Chat UI</title>
  <style>
     body {
      font-family: Arial, sans-serif;
      margin: 0;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      background: url('bg.png') no-repeat center center fixed;
      background-size: cover;
      position: relative;
    }

    .chat-popup {
      position: fixed;
      bottom: 20px;
      right: 20px;
      margin-right: 50px;
      border-radius: 50%;
    }
    .chat-popup img{
      width: 80px;
  height: 80px;
  border-radius: 50%; /* Ensures the image is a perfect circle */
  border: 3.5px solid #000; /* Correct way to add a visible black border */
  object-fit: cover; /* Ensures the image does not stretch or appear elliptical */
    }

    .chat-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
}

.navbar img {
  width: 50px;
  height: 50px;
  border-radius: 10px;
}

.navbar ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar ul li {
  margin: 0 15px;
}

.navbar ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
}

.navbar ul li a:hover {
  color: #00ff00;
}

.navbar .cta-button {
  background-color: #fff;
  color: #097969;
  border: 1px solid transparent;
  border-radius: 5px;
  padding: 8px 16px;
  text-decoration: none;
  font-weight: bold;
  cursor: pointer;
}

.navbar .cta-button:hover {
  background-color: #000;
  border: 1px solid #fff;
  color: #097969;
}

/* Responsive styles */
.navbar .hamburger {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  color: #fff;
  cursor: pointer;
}

@media (max-width: 768px) {
  .navbar ul {
    display: none; /* Hide navigation links initially */
    flex-direction: column;
    width: 100%;
    background-color: #000;
    position: absolute;
    top: 60px; /* Adjust based on navbar height */
    left: 0;
    padding: 0;
  }

  .navbar ul.show {
    display: flex; /* Show when toggled */
  }

  .navbar ul li {
    margin: 10px 0;
    text-align: center;
  }

  .navbar .hamburger {
    display: block; /* Show hamburger menu */
  }
}



    .chat-container {
  display: none;
  width: 400px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  flex-direction: column;
  overflow: hidden;
  position: absolute;
  bottom: 60px;
  right: 0;
  margin-right: 10px;
  z-index: 1000;
}
    .chat-header {
      display: flex;
      align-items: center;
      padding: 10px;
      background-color: #fff;
      color: #000;
    }
    /* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #f1f1f1}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {
  display: block;
}

    .chat-header img {
      margin-left: 138px;
  width: 40px;
  height: 40px;
  border-radius: 50%; /* Ensures the image is a perfect circle */
  border: 3px solid #000; /* Correct way to add a visible black border */
  object-fit: cover; /* Ensures the image does not stretch or appear elliptical */
}

    .chat-header span {
      margin-left: 10px;
    }
    .chat-content {
  padding: 15px;
  height: 300px;
  max-height: 500px;
  overflow-y: auto;
  background-color: #f9f9f9;
}
    .chat-bubble {
      max-width: 80%;
      padding: 10px;
      margin: 5px 0;
      border-radius: 10px;
      word-wrap: break-word;
      background-color: #8E8E8E;
    }
    .user-message {
      background-color: #8E8E8E;
      color: #fff;
      align-self: flex-end;
    }
    .bot-message {
      background-color: #e0e0e0;
      color: #333;
      align-self: flex-start;
    }
  
    .chat-input::placeholder {
  color: white; /* Set placeholder color to white */
  opacity: 0.7; /* Optional: Make placeholder text slightly translucent */
}
    .chat-input-container {
  display: flex;
  align-items: center;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #f5f5f5;
}
.chat-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background-color: #8E8E8E;
}

    .voice-input-button {
      background: none;
      border: none;
      cursor: pointer;
      color: #007bff;
      font-size: 20px;
      margin-left: 10px;
    }
    .voice-input-button:disabled {
      color: #cccccc;
      cursor: not-allowed;
    }
    .voice-status {
      font-size: 12px;
      color: #666;
      margin-left: 10px;
    }

    .send-button {
      margin-left: 10px;
      background: none;
      border: none;
      cursor: pointer;
      color: #007bff;
      font-size: 20px;
    }
    .powered-by-text {
      text-align: center;
      color: #555;
      font-size: 12px;
      margin: 10px 0;
    }


    .signup-container input {
  width: 80%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #E8E8E8;
  color: white;
}

.signup-container form label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}
  </style>

<script>

    
  
  function toggleChat() {
  const chatContainer = document.querySelector('.chat-container');
  if (!chatContainer) {
    console.error('Chat container element not found.');
    return;
  }

  if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
    chatContainer.style.display = 'block';
  } else {
    chatContainer.style.display = 'none';
  }
}



// Function to toggle the navbar visibility
function toggleNavbar() {
  const navbarList = document.getElementById('navbar-list');
  // Add or remove the "show" class to display or hide the menu
  navbarList.classList.toggle('show');
}

function toggleChat() {
      const introChat = document.querySelector('.intro-chat-container');
      const mainChat = document.querySelector('.main-chat-container');

      // Show the intro chat if both are hidden
      if (introChat.style.display === 'none' && mainChat.style.display === 'none') {
        introChat.style.display = 'block';
      } else {
        // Toggle visibility of both containers
        introChat.style.display = 'none';
        mainChat.style.display = 'none';
      }
    }

    function toggleChatMain(){
      const introChat = document.querySelector('.intro-chat-container');
      const mainChat = document.querySelector('.main-chat-container');

      // Show the intro chat if both are hidden
      if (introChat.style.display === 'none' && mainChat.style.display === 'none') {
        introChat.style.display = 'block';
      } else {
        // Toggle visibility of both containers
        introChat.style.display = 'none';
        mainChat.style.display = 'none';
      }
    }
    function handleSignupForm(event) {
    event.preventDefault(); // Prevents page refresh
    showMainChat(); // Opens the main chat container
  }

    function showMainChat() {
      const introChat = document.querySelector('.intro-chat-container');
      const mainChat = document.querySelector('.main-chat-container');

      // Hide the intro container and show the main chat
      introChat.style.display = 'none';
      mainChat.style.display = 'block';
    }

    function showSignup() {
  const introChat = document.querySelector('.intro-chat-container');
  const signupContainer = document.querySelector('.signup-container');

  // Hide the Intro Chat container and show the Sign-Up container
  introChat.style.display = 'none';
  signupContainer.style.display = 'block';
}

    function navigateToIntro() {
  const signupContainer = document.querySelector('.signup-container');
  const introChat = document.querySelector('.intro-chat-container');

  // Hide the Sign-Up container and show the Intro Chat container
  signupContainer.style.display = 'none';
  introChat.style.display = 'block';
}

// Function to toggle the dropdown visibility
function toggleDropdown() {
  const dropdown = document.getElementById('dropdown-menu');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

// Example functions for dropdown options
function sendProposal() {
  alert('SEND PROPOSAL clicked');
}

function toggleSounds() {
  alert('SOUNDS clicked');
}


</script>


</head>
<body>
  <!-- Navigation Bar -->
  <div class="navbar">
  <img src="npontuLogo.png" alt="Npontu Technologies Logo">
  <!-- Hamburger Menu Button -->
  <button class="hamburger" onclick="toggleNavbar()">☰</button>
  <ul id="navbar-list">
    <li><a href="#">Home</a></li>
    <li><a href="#">Company</a></li>
    <li><a href="#">Services</a></li>
    <li><a href="#">Resources</a></li>
    <li><a href="#">Partners</a></li>
    <li><a href="#">Blog</a></li>
    <li><a href="#">Jobs & Careers</a></li>
  </ul>
  <a href="#" class="cta-button">Let’s Talk</a>
</div>

<!-- Intro Chat Container -->
<div class="intro-chat-container chat-container" style="display: none;">
<div class="chat-header" style="background-color:#5CAB3F;">
  <div class="dropdown" class="dropbtn" style="margin-left: 10px; " >
  ...
  <div class="dropdown-content">
  <div class="dropdown-item" onclick="sendProposal()"> <a href="#" style="font-size: 13px;">📄SEND PROPOSAL</a></div>
  <div class="dropdown-item" onclick="toggleSounds()"> <a href="#" style="font-size: 13px;" >🔔 SOUNDS</a> </div>
  </div>
</div>
      <img src="picture.png" alt="Profile">
      <span style="margin-left: 130px; cursor: pointer;" onclick="toggleChat()">—</span>
    </div>
    <div class="chat-content" style="padding: 20px; text-align: center; font-size: 16px;">
      <p>Boost Your Business with us<br>
      From IT Consultancy and Managed Services to Big Data, AI to Platform and App Development! Do you want more information?</p>
      <p>My name is Peter Annan, and I am here for you.</p>
    </div>
    <div style="text-align: center; margin-bottom: 20px;">
    <button onclick="showMainChat()" style="padding: 10px 20px; background-color:#5CAB3F; color: white; border: none; border-radius: 5px; cursor: pointer;">Chat with Me</button>
    <button onclick="showSignup()" style="padding: 10px 20px; background-color: #ff0000; color: white; border: none; border-radius: 5px; cursor: pointer;">Apply Now</button>

    </div>
  </div>

 <!-- Chat Popup Button -->
 <div class="chat-popup">
  <button class="chat-button" onclick="toggleChat()">
    <img src="picture.png" alt="Profile" class="chat-toggle-image">
  </button>
</div>

<!-- Sign-Up Container -->
<div class="signup-container chat-container" class="main-chat-container chat-container" style="display: none; background-color: #f9f9f9">
 <div class="chat-header" style="background-color:#fff;  height:70px; ">
  
 <span style="cursor: pointer; font-size: 20px;" onclick="navigateToIntro()">←</span>
      <img src="picture.png" alt="Profile">
      <span style="margin-left: 130px; cursor: pointer;" onclick="toggleChatMain()">—</span>
    </div>
    <div class="chat-content">
    <p>Welcome to our LiveChat! Please fill in the form below before starting the chat.</p>
    <form onsubmit="return handleSignupForm(event)">
      <label for="name">Name:*</label>
      <input type="text" id="name" placeholder="Enter your name"  style="color: white; ">
      <br>
      <label for="email">Email: (Must be a VALID E-mail address)*</label>
      <input type="email" id="email" placeholder="Enter your email" style="color: white;">
      <br><br>
      <button onclick="showMainChat()"  style="padding: 10px 20px; background-color: red; color: white; border: none; border-radius: 5px; cursor: pointer;">Submit</button>
    </form>
    </div>
    <div class="powered-by-text">Powered by Npontu</div>
  </div>


    
  <!-- Chat UI -->
 <!-- Main Chat Container -->
 <div class="main-chat-container chat-container" style="display: none;">
 <div class="chat-header">
  <div class="dropdown" class="dropbtn" style="margin-left: 10px;">
  ...
  <div class="dropdown-content">
  <div class="dropdown-item" onclick="sendProposal()"> <a href="#" style="font-size: 13px;">📄SEND PROPOSAL</a></div>
  <div class="dropdown-item" onclick="toggleSounds()"> <a href="#" style="font-size: 13px;" >🔔 SOUNDS</a> </div>
  </div>
</div>
      <img src="picture.png" alt="Profile">
      <span style="margin-left: 130px; cursor: pointer;" onclick="toggleChat()">—</span>
    </div>
    <div class="chat-content">
      <div class="chat-bubble bot-message">
        Welcome! Please select an option above to get started:
      </div>
    </div>
    <div class="chat-input-container">
      <input type="text" class="chat-input" placeholder="Type a message...">
      <button class="send-button">&#9993;</button>
      <button class="voice-input-button" aria-label="Voice Input">🎤</button>
      <span class="voice-status" aria-live="polite"></span>
    </div>
    <div class="powered-by-text">Powered by Npontu</div>
  </div>

  
  <script>


    document.addEventListener('DOMContentLoaded', function () {
      const input = document.querySelector('.chat-input');
      const sendButton = document.querySelector('.send-button');
      const voiceButton = document.querySelector('.voice-input-button');
      const voiceStatus = document.querySelector('.voice-status');
      const chatContent = document.querySelector('.chat-content');
      const chatContainer = document.getElementById('chatContainer');

     

      // Speech Recognition Setup
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      let recognition = null;

      // Check if browser supports speech recognition
      if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US'; // You can change this to support other languages

        recognition.onstart = () => {
          voiceStatus.textContent = 'Listening...';
          voiceButton.disabled = true;
        };

        recognition.onresult = (event) => {
          const speechResult = event.results[0][0].transcript;
          input.value = speechResult;
          voiceStatus.textContent = '';
          voiceButton.disabled = false;
        };

        recognition.onerror = (event) => {
          voiceStatus.textContent = 'Error occurred in recognition: ' + event.error;
          voiceButton.disabled = false;
        };

        recognition.onend = () => {
          voiceStatus.textContent = '';
          voiceButton.disabled = false;
        };
      } else {
        // Disable voice input if not supported
        voiceButton.disabled = true;
        voiceStatus.textContent = 'Voice input not supported';
      }

      // Voice input button click handler
      voiceButton.addEventListener('click', () => {
        if (recognition) {
          try {
            recognition.start();
          } catch (error) {
            voiceStatus.textContent = 'Error starting voice recognition: ' + error;
          }
        }
      });

      const addMessage = (message, isUser) => {
        const bubble = document.createElement('div');
        bubble.classList.add('chat-bubble');
        bubble.classList.add(isUser ? 'user-message' : 'bot-message');
        bubble.textContent = message;

        chatContent.appendChild(bubble);
        chatContent.scrollTop = chatContent.scrollHeight;
      };

      const handleButtonClick = (option) => {
        addMessage(`You selected: ${option}`, true);
        addMessage(`Let me assist you with ${option}...`, false);
      };

      const sendMessage = async () => {
        const message = input.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, true);
        input.value = '';

        // Show loading indicator
        const loadingBubble = document.createElement('div');
        loadingBubble.classList.add('chat-bubble', 'bot-message');
        loadingBubble.textContent = '...';
        chatContent.appendChild(loadingBubble);

        try {
          // Example API request - replace with your actual logic
         const response = await fetch("https://npontu-bot-production.up.railway.app/api/v1/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
       });

          const backendUrl = "<?php echo $backendUrl; ?>";
          const data = await response.json();

          chatContent.removeChild(loadingBubble);
          addMessage(data.reply || "Sorry, I couldn't understand that.", false);
        } catch (error) {
          // Handle errors
          chatContent.removeChild(loadingBubble);
          addMessage("An error occurred. Please try again later.", false);
          console.error("Error:", error);
        }
      };

      // Event listeners for sending messages
      sendButton.addEventListener('click', sendMessage);
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          sendMessage();
        }
      });

      



      // Expose handleButtonClick to global scope for inline onclick
      window.handleButtonClick = handleButtonClick;
    });
  </script>
