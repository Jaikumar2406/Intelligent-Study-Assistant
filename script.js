let currentChatType = '';
const API_BASE_URL = 'http://localhost:8000'; 
document.addEventListener('DOMContentLoaded', function() {
   
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    initializeChatbot();
});

function openChatbot(type) {
    currentChatType = type;
    const modal = document.getElementById('chatbot-modal');
    const title = document.getElementById('chatbot-title');
    const chatMessages = document.getElementById('chat-messages');

    // Set title based on chatbot type
    title.textContent = type === 'qa' ? 'Q&A Assistant' : 'Syllabus Assistant';

    // Clear previous messages
    chatMessages.innerHTML = '';

    // Add welcome message
    addBotMessage(getWelcomeMessage(type));

    modal.style.display = 'block';
    document.getElementById('chat-input').focus();
}

function closeChatbot() {
    document.getElementById('chatbot-modal').style.display = 'none';
}

function getWelcomeMessage(type) {
    if (type === 'qa') {
        return "Hello! I'm your Q&A Assistant. Ask me any academic questions about subjects, concepts, or topics you're studying at Rungta College. How can I help you today?";
    } else if (type === 'syllabus') {
        return "Welcome to the Syllabus Assistant! I can help you find information about course syllabi, subject details, and academic requirements for different programs at Rungta College. What would you like to know?";
    }
    return "Hello! How can I assist you today?";
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (message === '') return;

    addUserMessage(message);
    input.value = '';

    showTypingIndicator();

    try {
        const response = await getAIResponse(message, currentChatType);
        hideTypingIndicator();
        addBotMessage(response);
    } catch (error) {
        hideTypingIndicator();
        addBotMessage("🚧 Sorry, I'm having trouble processing your request. Please try again later.");
    }
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = 'Assistant is typing...';
    typingDiv.id = 'typing-indicator';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) typingIndicator.remove();
}

async function getAIResponse(message, chatType) {
    try {
        const endpoint = chatType === 'qa' ? '/question' : '/syllabus';

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: message }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data.answer || " The assistant didn't return a valid response.";
    } catch (error) {
        console.error("API Request Failed:", error);
        return "Sorry, the assistant is temporarily unavailable. Please try again later.";
    }
}

// Initialize chatbot system
function initializeChatbot() {
    console.log('AI Chatbot Assistant initialized.');
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('chatbot-modal');
    if (event.target === modal) {
        closeChatbot();
    }
};

// Scroll animations
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = '#fff';
        navbar.style.backdropFilter = 'none';
    }
});

// Feature cards animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function() {
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});
