// Global variables
let currentChatType = '';
// const API_BASE_URL = 'https://jsonplaceholder.typicode.com'; // Mock API for demonstration

// Navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
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

    // Initialize chatbot with welcome message
    initializeChatbot();
});

// Chatbot functionality
function openChatbot(type) {
    currentChatType = type;
    const modal = document.getElementById('chatbot-modal');
    const title = document.getElementById('chatbot-title');
    const chatMessages = document.getElementById('chat-messages');
    
    // Set title based on chatbot type
    if (type === 'qa') {
        title.textContent = 'Q&A Assistant';
    } else if (type === 'syllabus') {
        title.textContent = 'Syllabus Assistant';
    }
    
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
    
    // Add user message
    addUserMessage(message);
    input.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate API call delay
    setTimeout(async () => {
        hideTypingIndicator();
        const response = await getAIResponse(message, currentChatType);
        addBotMessage(response);
    }, 1500);
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
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// AI Response simulation with API integration
async function getAIResponse(message, chatType) {
    try {
        // Mock API call - in real implementation, this would call your AI service
        const response = await fetch(`${API_BASE_URL}/posts/1`);
        const data = await response.json();
        
        // Generate contextual responses based on chat type and message
        return generateContextualResponse(message, chatType);
    } catch (error) {
        console.error('API Error:', error);
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again later.";
    }
}

function generateContextualResponse(message, chatType) {
    const lowerMessage = message.toLowerCase();
    
    if (chatType === 'qa') {
        // Q&A responses
        if (lowerMessage.includes('programming') || lowerMessage.includes('coding')) {
            return "Programming is a fundamental skill in engineering. At Rungta College, we cover languages like C, C++, Java, and Python. Which specific programming concept would you like to learn about?";
        } else if (lowerMessage.includes('mathematics') || lowerMessage.includes('math')) {
            return "Mathematics forms the foundation of engineering. Our curriculum includes Calculus, Linear Algebra, Differential Equations, and Statistics. What specific math topic can I help you with?";
        } else if (lowerMessage.includes('physics')) {
            return "Physics principles are crucial for understanding engineering concepts. We cover Mechanics, Thermodynamics, Electromagnetics, and Modern Physics. Which area interests you?";
        } else if (lowerMessage.includes('chemistry')) {
            return "Chemistry is essential for materials science and chemical processes in engineering. Our syllabus includes Organic, Inorganic, and Physical Chemistry. What would you like to know?";
        } else if (lowerMessage.includes('project') || lowerMessage.includes('assignment')) {
            return "For projects and assignments, I recommend starting with proper planning, research, and implementation. What type of project are you working on? I can provide specific guidance.";
        } else {
            return "That's an interesting question! Based on the Rungta College curriculum, I'd suggest exploring this topic through our library resources and lab sessions. Could you provide more specific details about what you'd like to learn?";
        }
    } else if (chatType === 'syllabus') {
        // Syllabus responses
        if (lowerMessage.includes('computer science') || lowerMessage.includes('cse')) {
            return "Computer Science Engineering syllabus includes:\n• Programming Languages (C, C++, Java, Python)\n• Data Structures & Algorithms\n• Database Management Systems\n• Computer Networks\n• Software Engineering\n• Machine Learning\n• Web Development\n\nWhich semester or subject would you like detailed information about?";
        } else if (lowerMessage.includes('mechanical') || lowerMessage.includes('mech')) {
            return "Mechanical Engineering syllabus covers:\n• Engineering Mechanics\n• Thermodynamics\n• Fluid Mechanics\n• Machine Design\n• Manufacturing Processes\n• Heat Transfer\n• Automotive Engineering\n\nWhich specific subject interests you?";
        } else if (lowerMessage.includes('electrical') || lowerMessage.includes('eee')) {
            return "Electrical Engineering syllabus includes:\n• Circuit Analysis\n• Power Systems\n• Control Systems\n• Electronics\n• Electromagnetic Theory\n• Digital Signal Processing\n• Renewable Energy Systems\n\nWhat specific area would you like to explore?";
        } else if (lowerMessage.includes('civil')) {
            return "Civil Engineering syllabus covers:\n• Structural Engineering\n• Geotechnical Engineering\n• Transportation Engineering\n• Environmental Engineering\n• Construction Management\n• Surveying\n• Hydraulics\n\nWhich subject do you need information about?";
        } else if (lowerMessage.includes('semester') || lowerMessage.includes('year')) {
            return "Our engineering programs are structured across 8 semesters (4 years). Each semester has core subjects, electives, and practical sessions. Which semester and branch are you interested in?";
        } else {
            return "I can provide detailed syllabus information for all engineering branches at Rungta College including Computer Science, Mechanical, Electrical, Civil, and Electronics. Which specific branch or subject would you like to know about?";
        }
    }
    
    return "Thank you for your question! I'm here to help with academic queries and syllabus information for Rungta College of Engineering and Technology. Could you please be more specific about what you'd like to know?";
}

// Additional API functions for fetching college data
async function fetchCollegeNews() {
    try {
        const response = await fetch(`${API_BASE_URL}/posts`);
        const posts = await response.json();
        return posts.slice(0, 5); // Get first 5 posts as news items
    } catch (error) {
        console.error('Error fetching news:', error);
        return [];
    }
}

async function fetchFacultyInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/users`);
        const users = await response.json();
        return users.slice(0, 10); // Get first 10 users as faculty
    } catch (error) {
        console.error('Error fetching faculty info:', error);
        return [];
    }
}

// Initialize chatbot system
function initializeChatbot() {
    console.log('Intelligent Study Assistant initialized for Rungta College of Engineering and Technology');
    
    // You can add initialization code here
    // For example, loading user preferences, chat history, etc.
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('chatbot-modal');
    if (event.target === modal) {
        closeChatbot();
    }
}

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

// Observe feature cards when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});