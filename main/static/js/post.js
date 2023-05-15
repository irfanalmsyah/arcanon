const sendAjaxRequest = (method, url, headers = {}, body = null) => {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    headers['X-CSRFToken'] = csrfToken;
        return fetch(url, { method, headers, body })
        .then(response => response.json())
        .catch(error => console.error(error));
};

const commentForm = document.querySelector('#comment-form');
commentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const url = event.target.action;
    const method = 'POST';
    const body = new FormData(event.target);
    sendAjaxRequest(method, url, {}, body)
        .then(data => {
        // Add the new comment to the comments list
        const commentsList = document.querySelector('#comments-list');
        const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const newComment = `
            <li id="comment-${data.id}">
                <div class="card mb-4">
                    <div class="card-body ps-4 pe-5">
                        <div class="row mb-2">
                            <div class="post-time">
                                Posted by you just now
                            </div>
                        </div>
                        <div class="row">
                            <div class="post-content">
                                ${data.content}
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="post-buttons d-flex">
                                <form method="POST" action="/forum/${data.post_id}/comment/${data.id}/like/" class="comment-like-form">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                                    <input type="hidden" name="comment_id" value="${data.id}">
                                    <button type="submit" id="like-button-${data.id}" class="btn btn-outline-secondary btn-sm me-2"><i class="bi bi-hand-thumbs-up"></i> <span id="likes-count-${data.id}">0</span> Likes</button>
                                </form>
                                <div class="dropdown ms-auto">
                                    <button class="btn btn-outline-none btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                                        <li><a class="dropdown-item" href="#">Report</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        `;
        commentsList.insertAdjacentHTML('afterbegin', newComment);
        const commentsCountElement = document.querySelector('#comments-count');
        const currentCount = parseInt(commentsCountElement.innerText);
        commentsCountElement.innerText = currentCount + 1;
        // Reset the comment form
        event.target.reset();
        });
});

const likeForm = document.querySelector('#like-form');
likeForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const url = event.target.action;
    const method = 'POST';
    sendAjaxRequest(method, url)
    .then(data => {
        // Update the like button style and the like count based on the response
        const likeButton = document.querySelector('#like-button');
        const likesCount = document.querySelector('#likes-count');
        if (data.liked) {
            likeButton.classList.remove('btn-outline-secondary');
            likeButton.classList.add('btn-secondary');
            likesCount.textContent = data.likes;
        } else {
            likeButton.classList.remove('btn-secondary');
            likeButton.classList.add('btn-outline-secondary');
            likesCount.textContent = data.likes;
        }
    });
});

const commentsList = document.querySelector('#comments-list');
commentsList.addEventListener('submit', (event) => {
    if (event.target.matches('.comment-like-form')) {
        event.preventDefault();
        const url = event.target.action;
        const method = 'POST';
        sendAjaxRequest(method, url)
        .then(data => {
            // Update the like button style and the like count based on the response
            const commentId = data.comment_id;
            const likeButton = document.querySelector(`#like-button-${commentId}`);
            const likesCount = document.querySelector(`#likes-count-${commentId}`);
            if (data.liked) {
                likeButton.classList.remove('btn-outline-secondary');
                likeButton.classList.add('btn-secondary');
                likesCount.textContent = data.likes;
            } else {
                likeButton.classList.remove('btn-secondary');
                likeButton.classList.add('btn-outline-secondary');
                likesCount.textContent = data.likes;
            }
        });
    }
});