// scripts.js

async function sendMessage() {
    const chatBody = document.getElementById('chatBody');
    const userInput = document.getElementById('userInput');

    const userMessage = userInput.value;
    if (userMessage.trim() === '') return;

    // Append user's message
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user';
    userMessageElement.innerHTML = `<div class="text">${userMessage}</div>`;
    chatBody.appendChild(userMessageElement);

    // Clear the input
    userInput.value = '';

    // Send message to the backend
    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: userMessage }),
        });

        // Check for a successful response
        if (!response.ok) {
            const errorText = await response.text(); // Get the error text for debugging
            throw new Error(`Network response was not ok: ${errorText}`);
        }

        const data = await response.json();

        // Append bot's response
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message bot';
        botMessageElement.innerHTML = `<div class="text">${data.response}</div>`;
        chatBody.appendChild(botMessageElement);

    } catch (error) {
        console.error('Error:', error);
        const errorMessageElement = document.createElement('div');
        errorMessageElement.className = 'message bot';
        errorMessageElement.innerHTML = `<div class="text">Sorry, there was an error: ${error.message}</div>`;
        chatBody.appendChild(errorMessageElement);
    }

    // Scroll to the bottom
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Event listener for Enter key
document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});
