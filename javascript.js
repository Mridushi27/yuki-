// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const healthForm = document.getElementById('health-form');
const predictionResults = document.getElementById('prediction-results');
const loadingOverlay = document.getElementById('loading-overlay');
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

// Tab Switching
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.getAttribute('data-tab');
        
        // Update active states
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        button.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});

// Chat Functionality
async function sendMessage(message) {
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                context: {} // Add context if needed
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response from chatbot');
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Error sending message:', error);
        showError('Failed to get response from chatbot. Please try again.');
        return null;
        
    } finally {
        hideLoading();
    }
}

function appendMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'system'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Handle send button click and Enter key
sendButton.addEventListener('click', handleSendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
    }
});

async function handleSendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Clear input
    userInput.value = '';
    
    // Add user message to chat
    appendMessage(message, true);
    
    // Get and display bot response
    const response = await sendMessage(message);
    if (response && response.response) {
        appendMessage(response.response);
    }
}

// Health Data Form Handling
healthForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        showLoading();
        
        // Gather form data
        const formData = new FormData(healthForm);
        const healthData = {
            blood_glucose: parseFloat(formData.get('blood_glucose')) || null,
            systolic_bp: parseFloat(formData.get('systolic_bp')) || null,
            diastolic_bp: parseFloat(formData.get('diastolic_bp')) || null,
            heart_rate: parseFloat(formData.get('heart_rate')) || null,
            age: parseInt(formData.get('age')) || null,
            bmi: parseFloat(formData.get('bmi')) || null,
            medical_history: formData.get('medical_history')
                ? formData.get('medical_history').split(',').map(item => item.trim())
                : []
        };
        
        // Send data to API
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(healthData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to get health risk prediction');
        }
        
        const data = await response.json();
        displayPredictions(data.predictions);
        
    } catch (error) {
        console.error('Error submitting health data:', error);
        showError('Failed to get health risk prediction. Please try again.');
        
    } finally {
        hideLoading();
    }
});

function displayPredictions(predictions) {
    const resultsContainer = predictionResults.querySelector('.results-container');
    resultsContainer.innerHTML = ''; // Clear previous results
    
    // Create risk cards for each prediction
    for (const [condition, data] of Object.entries(predictions)) {
        const riskCard = document.createElement('div');
        riskCard.className = 'risk-card';
        
        // Determine risk level
        let riskLevel = 'low';
        if (data.risk_score >= 70) riskLevel = 'high';
        else if (data.risk_score >= 40) riskLevel = 'medium';
        
        riskCard.innerHTML = `
            <h3>${condition.charAt(0).toUpperCase() + condition.slice(1)}</h3>
            <div class="risk-score ${riskLevel}">
                Risk Score: ${data.risk_score}%
            </div>
            <p>${data.recommendation}</p>
        `;
        
        resultsContainer.appendChild(riskCard);
    }
    
    // Scroll to results
    predictionResults.scrollIntoView({ behavior: 'smooth' });
}

// Loading Overlay
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Error Handling
function showError(message) {
    const errorTemplate = document.querySelector('.error-template');
    const errorDiv = errorTemplate.cloneNode(true);
    errorDiv.classList.remove('error-template');
    errorDiv.style.display = 'block';
    
    const errorMessage = errorDiv.querySelector('p');
    errorMessage.textContent = message;
    
    const closeButton = errorDiv.querySelector('.close-error');
    closeButton.addEventListener('click', () => {
        errorDiv.remove();
    });
    
    // Add error message to the top of the current tab
    const activeTab = document.querySelector('.tab-content.active');
    activeTab.insertBefore(errorDiv, activeTab.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check if API is available
    fetch(`${API_BASE_URL}/health-check`)
        .catch(error => {
            console.error('API not available:', error);
            showError('Unable to connect to the server. Please try again later.');
        });
});
