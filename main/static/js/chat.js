const roomNameEl = document.getElementById('room-name');
const userEl = document.getElementById('user');
const chatPanelEl = document.querySelector('#chat-panel');
const messageInputEl = document.querySelector('#message-input');
const messageSendEl = document.querySelector('#message-send');
const endBtn = document.querySelector('#end');

const roomName = JSON.parse(roomNameEl.textContent);
const user = JSON.parse(userEl.textContent);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

chatSocket.onmessage = function(event) {
const data = JSON.parse(event.data);
if (data.message) {
    const className = data.user === 'You' ? 'chat-bubble-right' : 'chat-bubble-left';
    const chatBubbleEl = document.createElement('div');
    chatBubbleEl.classList.add(className);
    chatBubbleEl.innerHTML = `<p>${data.message}</p>`;
    chatPanelEl.appendChild(chatBubbleEl);
    chatPanelEl.scrollTop = chatPanelEl.scrollHeight;
} else {
    alert('Stranger has left the room');
    disconnect();
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
    chatSocket.send(JSON.stringify({
        user: user,
        message: message
    }));
    messageInputEl.value = '';
});

endBtn.addEventListener('click', function() {
    chatSocket.send(JSON.stringify({
        user: user,
        destroy: 1
    }));
    disconnect();
});

function disconnect() {
    chatSocket.close();
    window.location.href = '/';
}