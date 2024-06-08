window.onload = function () {
  // Initialize the Ace Editor for functions
  const functionsEditor = ace.edit('functions-editor');
  functionsEditor.setTheme('ace/theme/github');
  functionsEditor.session.setMode('ace/mode/json');
  functionsEditor.setOptions({
    maxLines: 20, // Increase the maximum number of lines to show by default
    autoScrollEditorIntoView: true,
    wrap: true, // Enable wrapping to prevent horizontal scrolling
    minLines: 15, // Ensure the editor shows at least this many lines initially
  });

  // Event listener to add function JSON
  document
    .getElementById('add-function')
    .addEventListener('click', function () {
      const jsonValue = functionsEditor.getValue();
      if (jsonValue) {
        console.log('Function added:', jsonValue);
        // TODO: Add logic to handle the added function JSON here
      }
    });

  // Handle keypress events in the chat message input
  const messageInput = document.getElementById('chat-message');
  messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      // Prevent the default action (new line)
      event.preventDefault();
      // Send the message
      sendMessage();
    }
  });
};

async function sendMessage() {
  const messageInput = document.getElementById('chat-message');
  const message = messageInput.value;
  const chatOutput = document.getElementById('chat-messages');
  const loader = document.getElementById('loader');

  if (!message) {
    alert('Please enter a message.');
    return;
  }

  // Clear the input field after sending the message
  messageInput.value = '';

  // Display the user's message
  const userMessageElement = document.createElement('div');
  userMessageElement.classList.add('user-message');
  userMessageElement.textContent = `User: ${message}`;
  chatOutput.appendChild(userMessageElement);

  // Show loader
  loader.style.display = 'block';

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/chat?message=${encodeURIComponent(message)}`,
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      }
    );

    // Hide loader if no response body
    if (!response.body) {
      throw new Error('No response body available.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;

    // Create an element to hold the AI response
    const aiMessageElement = document.createElement('div');
    aiMessageElement.classList.add('ai-message');
    aiMessageElement.textContent = 'AI: ';
    chatOutput.appendChild(aiMessageElement);

    // Read the response stream
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      const chunk = decoder.decode(value, { stream: true });

      // Append the chunk to the AI message element
      aiMessageElement.textContent += chunk;
      chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom
    }
  } catch (error) {
    const errorElement = document.createElement('div');
    errorElement.classList.add('error-message');
    errorElement.innerHTML = `<strong>Error:</strong> ${error.message}`;
    chatOutput.appendChild(errorElement);
  } finally {
    // Hide loader when the process is complete
    loader.style.display = 'none';
  }
}
