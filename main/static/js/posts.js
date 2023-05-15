

const postsList = document.querySelector('#posts-list');
postsList.addEventListener('submit', (event) => {
    if (event.target.matches('.like-form')) {
        event.preventDefault();
        const url = event.target.action;
        const method = 'POST';
        sendAjaxRequest(method, url)
        .then(data => {
            // Update the like button style and the like count based on the response
            const postId = data.post_id;
            const likeButton = document.querySelector(`#like-button-${postId}`);
            const likesCount = document.querySelector(`#likes-count-${postId}`);
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