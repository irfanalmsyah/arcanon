const roomNameEl = document.getElementById('room-name');
const userEl = document.getElementById('user');
const chatPanelEl = document.querySelector('#chat-panel');
const messageInputEl = document.querySelector('#message-input');
const messageSendEl = document.querySelector('#message-send');
const endBtn = document.querySelector('#end');
const revealBtn = document.querySelector('#reveal');

const roomName = JSON.parse(roomNameEl.textContent);
const user = JSON.parse(userEl.textContent);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

chatSocket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const type = data.type;
    if (type === 'message') {
        const className = data.user === 'You' ? 'chat-bubble-right' : 'chat-bubble-left';
        const chatBubbleEl = document.createElement('div');
        chatBubbleEl.classList.add(className);
        chatBubbleEl.innerHTML = `<p>${data.message}</p>`;
        chatPanelEl.appendChild(chatBubbleEl);
        chatPanelEl.scrollTop = chatPanelEl.scrollHeight;
    } else if (type === 'destroy') {
        alert('Stranger has left the room');
        disconnect();
    } else if (type === 'reveal_request') {
        if (confirm('Stranger wants to reveal their identity. Do you want to reveal your identity?')) {
            chatSocket.send(JSON.stringify({
                type: 'reveal_response',
                user: user,
                reveal: true
            }));
        } else {
            chatSocket.send(JSON.stringify({
                type: 'reveal_response',
                user: user,
                reveal: false
            }));
        }
    }  else if (type === 'identity') {
        const revealCardEl = document.querySelector('#reveal-card');
        const strangerPictureEl = document.querySelector('#stranger-picture');
        const identityFirstEl = document.querySelector('#identity-first');
        const identitySecondEl = document.querySelector('#identity-second');
        const identityThirdEl = document.querySelector('#identity-third');
        revealCardEl.style.display = 'block';
        strangerPictureEl.src = data.picture;
        const flag = (data.country).toUpperCase()
        .replace(/./g, char => String.fromCodePoint(char.charCodeAt(0) + 127397));
        identityFirstEl.textContent = flag + ' ' + data.name;
        identitySecondEl.textContent = data.instagram;
        identityThirdEl.textContent = data.twitter;
        revealBtn.style.display = 'none';
    } else if (type === 'reveal_request_you_not_complete') {
        alert('You have not completed your profile. Please complete your profile to reveal your identity');
    } else if (type === 'reveal_request_stranger_not_complete') {
        alert('Stranger has not completed their profile. Please wait for them to complete their profile');
    } else if (type === 'reveal_response_rejected') {
        alert('Stranger has rejected your request to reveal their identity');
    }
};

chatSocket.onclose = function() {
    console.error('Chat socket closed unexpectedly');
};

messageInputEl.focus();

messageInputEl.addEventListener('keyup', function(event) {
    if (event.keyCode === 13) { 
        messageSendEl.click();
    }
});

messageSendEl.addEventListener('click', function() {
    const message = messageInputEl.value;
    if (message.trim() === '') {
        return;
    }
    chatSocket.send(JSON.stringify({
        type: 'message',
        user: user,
        message: message
    }));
    messageInputEl.value = '';
});

endBtn.addEventListener('click', function() {
    chatSocket.send(JSON.stringify({
        type: 'destroy',
        user: user,
    }));
    disconnect();
});

revealBtn.addEventListener('click', function() {
    chatSocket.send(JSON.stringify({
        type: 'reveal_request',
        user: user,
    }));
});

function disconnect() {
    chatSocket.close();
    window.location.href = '/';
}