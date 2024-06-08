async function sendMessage() {
  const messageInput = document.getElementById('chat-message');
  const message = messageInput.value;
  const chatOutput = document.getElementById('chat-messages');

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

  try {
    // Fetch the streaming response
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

    if (!response.body) {
      const errorElement = document.createElement('div');
      errorElement.classList.add('error-message');
      errorElement.innerHTML =
        '<strong>Error:</strong> No response body available.';
      chatOutput.appendChild(errorElement);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;

    // Create an element to hold the AI response
    const aiMessageElement = document.createElement('div');
    aiMessageElement.classList.add('ai-message');
    aiMessageElement.textContent = 'AI: ';
    chatOutput.appendChild(aiMessageElement);

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
  }
}
