document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

var animateButton = function(e) {
    e.preventDefault();
    //reset animation
    e.target.classList.remove('animate');
    e.target.classList.add('animate');
    setTimeout(function(){
        e.target.classList.remove('animate');
    }, 700);
};

var bubblyButtons = document.getElementsByClassName("bubbly-button");

for (var i = 0; i < bubblyButtons.length; i++) {
    bubblyButtons[i].addEventListener('click', animateButton, false);
}

document.getElementById('chat-popup-button').addEventListener('click', function() {
    let chatContainer = document.getElementById('chat-container');
    chatContainer.classList.toggle('hidden');
});

function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    let chatBox = document.getElementById('chat-box');
    let userMessage = document.createElement('div');
    userMessage.textContent = userInput;
    userMessage.className = 'user-message';
    chatBox.appendChild(userMessage);

    document.getElementById('user-input').value = '';

    fetch('/chatbot/get_response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        let botMessage = document.createElement('div');
        botMessage.textContent = data.response;
        botMessage.className = 'bot-message';
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
