window.onload = async function () {
  // Initialize the Ace Editor for functions
  const functionsEditor = ace.edit('functions-editor');
  functionsEditor.setTheme('ace/theme/github');
  functionsEditor.session.setMode('ace/mode/json');
  functionsEditor.setOptions({
    maxLines: 20,
    autoScrollEditorIntoView: true,
    wrap: true,
    minLines: 15,
  });

  // Generate a UUID-like context_id
  function generateUUID() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
      (
        c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
      ).toString(16)
    );
  }

  // Set the generated context_id in the textarea
  const contextId = generateUUID();
  document.getElementById('context_id').value = contextId;

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
      event.preventDefault();
      sendMessage();
    }
  });

  // Fetch the system prompt from the backend
  try {
    const response = await fetch('http://127.0.0.1:8000/api/system-prompt'); // Adjust URL as needed
    if (!response.ok) {
      throw new Error('Failed to fetch the system prompt.');
    }

    const data = await response.json();
    if (data && data.content) {
      document.getElementById('system-prompt').value = data.content;
    }
  } catch (error) {
    console.error('Error fetching system prompt:', error);
    alert(
      'Unable to fetch the system prompt. Please check the console for more details.'
    );
  }

  try {
    const toolResponse = await fetch('http://127.0.0.1:8000/api/tools');
    if (!toolResponse.ok) {
      throw new Error('Failed to fetch the tools.');
    }

    const toolData = await toolResponse.json();

    if (toolData && toolData.content && toolData.content.tools) {
      const tools = toolData.content.tools;
      functionsEditor.setValue(JSON.stringify(tools, null, 2));
    } else {
      alert('No tools data available.');
    }
  } catch (error) {
    console.error('Error fetching tools:', error);
    alert(
      'Unable to fetch the tools. Please check the console for more details.'
    );
  }
};

async function sendMessage() {
  const messageInput = document.getElementById('chat-message');
  const message = messageInput.value;
  const chatOutput = document.getElementById('chat-messages');
  const loader = document.getElementById('loader');
  const contextId = document.getElementById('context_id').value;

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
    // Create the request payload
    const payload = {
      context_id: contextId,
      message: message,
    };

    console.log('Sending payload:', payload);

    const response = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    // Check for response status
    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

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
    chatOutput.appendChild(aiMessageElement);

    let fullMessage = ''; // To accumulate the full response

    // Initialize Showdown converter
    const converter = new showdown.Converter();

    // Read the response stream
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      const chunk = decoder.decode(value, { stream: true });

      fullMessage += chunk; // Accumulate the chunks

      // Log the fullMessage to verify its content
      // console.log('AI Response (raw):', fullMessage);

      // Convert Markdown to HTML using Showdown.js
      try {
        const htmlContent = converter.makeHtml(fullMessage);
        aiMessageElement.innerHTML = htmlContent; // Set converted HTML
      } catch (renderingError) {
        // console.error('Error rendering Markdown:', renderingError);
        aiMessageElement.innerHTML = `<div class="error-message">Error rendering Markdown: ${renderingError.message}</div>`;
      }
      chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom
    }
  } catch (error) {
    console.error('Error during chat processing:', error);

    const errorElement = document.createElement('div');
    errorElement.classList.add('error-message');
    errorElement.innerHTML = `<strong>Error:</strong> ${error.message}`;
    chatOutput.appendChild(errorElement);
  } finally {
    // Hide loader when the process is complete
    loader.style.display = 'none';
  }
}
