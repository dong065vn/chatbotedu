/* ============================================
   Professional Chatbot JavaScript v2.0
   Advanced Features & Interactivity
   ============================================ */

// Application State
let isProcessing = false;
let messageCount = 0;
let chatHistory = [];
let darkMode = localStorage.getItem('darkMode') === 'true';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadChatHistory();
    updateStats();
});

// Initialize Application
function initializeApp() {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('messageInput');
    const initialTime = document.getElementById('initialTime');

    // Set initial timestamp
    if (initialTime) {
        initialTime.textContent = formatTime(new Date());
    }

    // Apply saved theme
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }

    // Show welcome notification
    setTimeout(() => {
        showNotification('Chào mừng bạn đến với Chatbot AI! 🎉', 'success');
    }, 1000);
}

// Setup Event Listeners
function setupEventListeners() {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('messageInput');
    const themeToggle = document.getElementById('themeToggle');
    const clearChat = document.getElementById('clearChat');
    const exportChat = document.getElementById('exportChat');
    const toggleSidebar = document.getElementById('toggleSidebar');
    const emojiButton = document.getElementById('emojiButton');
    const voiceInput = document.getElementById('voiceInput');

    // Form submission
    form.addEventListener('submit', handleFormSubmit);

    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Clear chat
    if (clearChat) {
        clearChat.addEventListener('click', handleClearChat);
    }

    // Export chat
    if (exportChat) {
        exportChat.addEventListener('click', handleExportChat);
    }

    // Toggle sidebar
    if (toggleSidebar) {
        toggleSidebar.addEventListener('click', handleToggleSidebar);
    }

    // Emoji picker
    if (emojiButton) {
        emojiButton.addEventListener('click', toggleEmojiPicker);
    }

    // Voice input
    if (voiceInput) {
        voiceInput.addEventListener('click', handleVoiceInput);
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);

    // Input focus on Ctrl+K
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });

    // Emoji picker items
    setupEmojiPicker();

    // Click outside to close emoji picker
    document.addEventListener('click', (e) => {
        const emojiPicker = document.getElementById('emojiPicker');
        const emojiBtn = document.getElementById('emojiButton');
        if (emojiPicker && !emojiPicker.contains(e.target) && e.target !== emojiBtn) {
            emojiPicker.style.display = 'none';
        }
    });
}

// Handle Form Submission
async function handleFormSubmit(e) {
    e.preventDefault();

    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isProcessing) return;

    // Clear input
    input.value = '';

    // Add user message to chat
    addMessage(message, 'user');
    messageCount++;
    updateStats();

    // Save to history
    chatHistory.push({ role: 'user', content: message, timestamp: new Date().toISOString() });
    saveChatHistory();

    // Show typing indicator
    const typingId = showTypingIndicator();

    // Update status
    updateStatus('Đang suy nghĩ...');

    // Send message to backend
    isProcessing = true;
    try {
        const response = await sendMessage(message);
        removeTypingIndicator(typingId);

        if (response.success) {
            addMessage(response.response, 'bot');
            chatHistory.push({ role: 'bot', content: response.response, timestamp: response.timestamp });
            saveChatHistory();
            updateStats();
        } else {
            addMessage('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.', 'bot');
            showNotification('Đã xảy ra lỗi khi xử lý tin nhắn', 'error');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Không thể kết nối đến server. Vui lòng kiểm tra kết nối.', 'bot');
        showNotification('Lỗi kết nối đến server', 'error');
        console.error('Error:', error);
    } finally {
        isProcessing = false;
        updateStatus('Đang hoạt động');
    }

    // Focus input
    input.focus();
}

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

    // Scroll to bottom with smooth animation
    scrollToBottom();

    // Add animation
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease-out';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 10);
}

// Format message text with HTML
function formatMessageText(text) {
    // Convert line breaks to HTML
    let formatted = text.replace(/\n/g, '<br>');

    // Format bold text (if using **text**)
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Format italic text (if using *text*)
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Format code blocks
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Format links
    formatted = formatted.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');

    return formatted;
}

// Show typing indicator
function showTypingIndicator() {
    const typingArea = document.getElementById('typingArea');
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'typing-indicator';

    typingDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;

    typingArea.appendChild(typingDiv);
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
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
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

// Toggle Theme
function toggleTheme() {
    darkMode = !darkMode;
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', darkMode);
    
    const message = darkMode ? 'Đã chuyển sang chế độ tối 🌙' : 'Đã chuyển sang chế độ sáng ☀️';
    showNotification(message, 'success');
}

// Handle Clear Chat
function handleClearChat() {
    if (confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử chat?')) {
        const messagesContainer = document.getElementById('chatMessages');
        
        // Keep only the welcome message
        const welcomeMessage = messagesContainer.querySelector('.message.bot-message');
        messagesContainer.innerHTML = '';
        if (welcomeMessage) {
            messagesContainer.appendChild(welcomeMessage);
        }
        
        // Reset history
        chatHistory = [];
        messageCount = 0;
        saveChatHistory();
        updateStats();
        
        showNotification('Đã xóa lịch sử chat thành công', 'success');
    }
}

// Handle Export Chat
function handleExportChat() {
    if (chatHistory.length === 0) {
        showNotification('Không có dữ liệu chat để xuất', 'warning');
        return;
    }

    // Create export content
    let exportContent = 'LỊCH SỬ CHAT - CHATBOT QUẢN LÝ THỜI GIAN\n';
    exportContent += '='.repeat(50) + '\n';
    exportContent += `Ngày xuất: ${new Date().toLocaleString('vi-VN')}\n`;
    exportContent += `Tổng số tin nhắn: ${chatHistory.length}\n`;
    exportContent += '='.repeat(50) + '\n\n';

    chatHistory.forEach((msg, index) => {
        const timestamp = new Date(msg.timestamp).toLocaleString('vi-VN');
        const role = msg.role === 'user' ? 'BẠN' : 'BOT';
        exportContent += `[${timestamp}] ${role}:\n${msg.content}\n\n`;
    });

    // Create blob and download
    const blob = new Blob([exportContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-history-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Đã xuất lịch sử chat thành công', 'success');
}

// Handle Toggle Sidebar
function handleToggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth <= 1024) {
        sidebar.classList.toggle('visible');
    } else {
        sidebar.classList.toggle('hidden');
    }
}

// Toggle Emoji Picker
function toggleEmojiPicker() {
    const emojiPicker = document.getElementById('emojiPicker');
    if (emojiPicker.style.display === 'none' || !emojiPicker.style.display) {
        emojiPicker.style.display = 'block';
    } else {
        emojiPicker.style.display = 'none';
    }
}

// Setup Emoji Picker
function setupEmojiPicker() {
    const emojiItems = document.querySelectorAll('.emoji-item');
    const input = document.getElementById('messageInput');

    emojiItems.forEach(item => {
        item.addEventListener('click', () => {
            input.value += item.textContent;
            input.focus();
            document.getElementById('emojiPicker').style.display = 'none';
        });
    });
}

// Handle Voice Input
function handleVoiceInput() {
    showNotification('Tính năng nhập giọng nói đang được phát triển', 'warning');
    
    // Future implementation with Web Speech API
    /*
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'vi-VN';
        recognition.start();
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            document.getElementById('messageInput').value = transcript;
        };
    }
    */
}

// Keyboard Shortcuts
function handleKeyboardShortcuts(e) {
    // Ctrl+K: Focus input
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        document.getElementById('messageInput').focus();
    }
    
    // Ctrl+L: Clear chat
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        handleClearChat();
    }
    
    // Ctrl+D: Toggle dark mode
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        toggleTheme();
    }
    
    // Escape: Close emoji picker
    if (e.key === 'Escape') {
        document.getElementById('emojiPicker').style.display = 'none';
    }
}

// Update Status Text
function updateStatus(status) {
    const statusText = document.getElementById('statusText');
    if (statusText) {
        statusText.textContent = status;
    }
}

// Update Statistics
function updateStats() {
    const messageCountEl = document.getElementById('messageCount');
    const scheduleCountEl = document.getElementById('scheduleCount');
    const examCountEl = document.getElementById('examCount');

    if (messageCountEl) {
        messageCountEl.textContent = messageCount;
        animateValue(messageCountEl, 0, messageCount, 500);
    }

    // Fetch actual schedule and exam counts from API
    fetchStats();
}

// Fetch Statistics from API
async function fetchStats() {
    try {
        // This would call your backend API to get real stats
        // For now, we'll use placeholder values
        const scheduleCountEl = document.getElementById('scheduleCount');
        const examCountEl = document.getElementById('examCount');

        // Placeholder - replace with actual API call
        // const response = await fetch('/api/stats');
        // const data = await response.json();
        
        if (scheduleCountEl) scheduleCountEl.textContent = '0';
        if (examCountEl) examCountEl.textContent = '0';
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

// Animate Value (Counter Animation)
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Show Notification
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    container.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            container.removeChild(notification);
        }, 300);
    }, 3000);
}

// Save Chat History to LocalStorage
function saveChatHistory() {
    try {
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        localStorage.setItem('messageCount', messageCount);
    } catch (error) {
        console.error('Error saving chat history:', error);
    }
}

// Load Chat History from LocalStorage
function loadChatHistory() {
    try {
        const saved = localStorage.getItem('chatHistory');
        const savedCount = localStorage.getItem('messageCount');
        
        if (saved) {
            chatHistory = JSON.parse(saved);
        }
        
        if (savedCount) {
            messageCount = parseInt(savedCount, 10);
        }

        // Don't restore messages to UI, just keep the data
        // Users can start fresh but export will have full history
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Auto-save periodically
setInterval(saveChatHistory, 30000); // Save every 30 seconds

// Handle Page Visibility (pause/resume)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        updateStatus('Tạm dừng');
    } else {
        updateStatus('Đang hoạt động');
    }
});

// Online/Offline Detection
window.addEventListener('online', () => {
    updateStatus('Đang hoạt động');
    showNotification('Đã kết nối lại internet', 'success');
});

window.addEventListener('offline', () => {
    updateStatus('Mất kết nối');
    showNotification('Mất kết nối internet', 'error');
});

// Responsive Sidebar Auto-hide on Mobile
window.addEventListener('resize', () => {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('visible');
    }
});

// Export functions for HTML onclick handlers
window.sendSuggestion = sendSuggestion;

// Console Welcome Message
console.log('%c🤖 Chatbot Quản lý Thời gian v2.0', 'font-size: 20px; color: #667eea; font-weight: bold;');
console.log('%cProfessional Edition - Powered by Gemini AI', 'font-size: 12px; color: #764ba2;');
console.log('%c💡 Keyboard Shortcuts:', 'font-size: 14px; font-weight: bold; margin-top: 10px;');
console.log('Ctrl+K: Focus input');
console.log('Ctrl+L: Clear chat');
console.log('Ctrl+D: Toggle dark mode');
