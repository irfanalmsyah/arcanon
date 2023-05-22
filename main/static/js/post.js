const commentForm = document.querySelector('#comment-form');
commentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const url = event.target.action;
    const method = 'POST';
    const content = document.querySelector('#message-input').value;
    const body = `content=${encodeURIComponent(content)}`

    sendAjaxRequest(method, url, body)
        .then(data => {
        // Add the new comment to the comments list
        const commentsList = document.querySelector('#comments-list');
        const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const newComment = `
            <div class="modal fade" id="reportCommentModal-${data.id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Report</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                            <input type="text" class="form-control" id="report-input-${data.id}" placeholder="Please provide the reason for the report">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button class="report-toast-trigger btn btn-blue" onclick="report('comment', '${data.id}', document.getElementById('report-input-${data.id}').value)" type="button" class="btn btn-blue" data-bs-dismiss="modal">Report</button>
                        </div>
                    </div>
                </div>
            </div>
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
                                <form method="POST" action="/forum/${data.post_id}/comment/${data.id}/edit/" class="d-none" id="comment-form-${data.id}">
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                                    <div class="input-group mb-3">
                                        <input type="text" name="content" class="form-control" id="message-input" value="${data.content}">
                                        <button type="submit" class="btn btn-outline-blue" type="button" id="message-send"><i class="bi bi-send"></i></button>
                                    </div>
                                </form>
                                <span id="comment-content-${data.id}">
                                ${data.content}
                                </span>
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
                                        <li><button class="dropdown-item" onclick="editComment(${data.id})">Edit</button></li>
                                        <li><a class="dropdown-item" href="/forum/${data.post_id}/comment/${data.id}/delete/">Delete</a></li>
                                        <li><button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#reportCommentModal-${data.id}">Report</button></li>
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
        reportToastTrigger = document.querySelectorAll(".report-toast-trigger");
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

function editComment(id) {

    const commentContent = document.querySelector(`#comment-content-${id}`);
    const commentEditForm = document.querySelector(`#comment-form-${id}`);
    commentContent.classList.add('d-none');
    commentEditForm.classList.remove('d-none');
}