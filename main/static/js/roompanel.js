const requestBtn = document.getElementById('request');
const respondBtn = document.getElementById('respond');
const enterBtn = document.getElementById('enter');
const closeBtn = document.getElementById('close');
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const toast = document.getElementById('roomToast')
const xhr = new XMLHttpRequest();
(async () => {
    try {
        const response = await fetch('/chat/room/');
        if (!response.ok) {
            throw new Error('Request failed');
        }
        const loader = document.getElementById('loader');
        loader.style.display = 'none';
        const data = await response.json();
        if (data.room_name) {
            requestBtn.style.display = 'none';
            respondBtn.style.display = 'none';
            enterBtn.style.display = 'block';
            closeBtn.style.display = 'block';
        } else {
            enterBtn.style.display = 'none';
            closeBtn.style.display = 'none';
            requestBtn.style.display = 'block';
            respondBtn.style.display = 'block';
        }
    } catch (error) {
        console.error(error);
    }
})();  

requestBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/chat/create/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
            },
        });
        if (!response.ok) {
            throw new Error('Request failed');
        }
        const data = await response.json();
    
        if (data.room_name) {
            requestBtn.style.display = 'none';
            respondBtn.style.display = 'none';
            enterBtn.style.display = 'block';
            closeBtn.style.display = 'block';
            const enterAnchor = document.getElementById('enter-anchor');
            enterAnchor.classList.add('disabled');
        }
    } catch (error) {
        console.error(error);
    }
});

respondBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/chat/respond/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        });
        const data = await response.json();

        if (data.room_name) {
            requestBtn.style.display = 'none';
            respondBtn.style.display = 'none';
            enterBtn.style.display = 'block';
            closeBtn.style.display = 'block';
            const enterAnchor = document.getElementById('enter-anchor');
            enterAnchor.href = "/chat/room/" + data.room_name + "/";
            enterAnchor.classList.remove('disabled');
        } else {
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast)
            toastBootstrap.show()
        }
    } catch (error) {
      console.error(error);
    }
});
  
closeBtn.addEventListener('click', async function() {
    try {
        await fetch('/chat/close/');
        enterBtn.style.display = 'none';
        closeBtn.style.display = 'none';
        requestBtn.style.display = 'block';
        respondBtn.style.display = 'block';
    } catch (error) {
        console.error(error);
    }
});
  