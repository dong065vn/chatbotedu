// Chat application logic

let isProcessing = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('messageInput');
    const initialTime = document.getElementById('initialTime');

    // Set initial timestamp
    initialTime.textContent = formatTime(new Date());

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = input.value.trim();
        if (!message || isProcessing) return;

        // Clear input
        input.value = '';

        // Add user message to chat
        addMessage(message, 'user');

        // Show typing indicator
        const typingId = showTypingIndicator();

        // Send message to backend
        isProcessing = true;
        try {
            const response = await sendMessage(message);
            removeTypingIndicator(typingId);

            if (response.success) {
                addMessage(response.response, 'bot');
            } else {
                addMessage('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.', 'bot');
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage('Không thể kết nối đến server. Vui lòng kiểm tra kết nối.', 'bot');
            console.error('Error:', error);
        } finally {
            isProcessing = false;
        }

        // Focus input
        input.focus();
    });
});

// Send message to API
async function sendMessage(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    return await response.json();
}

// Add message to chat
function addMessage(text, type) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'bot' ? '🤖' : '👤';

    const content = document.createElement('div');
    content.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = formatMessageText(text);

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = formatTime(new Date());

    content.appendChild(textDiv);
    content.appendChild(timeDiv);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();
}

// Format message text with HTML
function formatMessageText(text) {
    // Convert line breaks to HTML
    let formatted = text.replace(/\n/g, '<br>');

    // Format bold text (if using **text**)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Format code blocks
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

    return formatted;
}

// Show typing indicator
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message bot-message';

    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(typingDiv);
    scrollToBottom();

    return id;
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format timestamp
function formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Send suggestion (called from HTML buttons)
function sendSuggestion(text) {
    const input = document.getElementById('messageInput');
    input.value = text;
    document.getElementById('chatForm').dispatchEvent(new Event('submit'));
}

// Auto-resize input (optional enhancement)
const input = document.getElementById('messageInput');
if (input) {
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.getElementById('chatForm').dispatchEvent(new Event('submit'));
        }
    });
}
