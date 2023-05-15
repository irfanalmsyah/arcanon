const sendAjaxRequest = (method, url, headers = {}, body = null) => {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    headers['X-CSRFToken'] = csrfToken;
        return fetch(url, { method, headers, body })
        .then(response => response.json())
        .catch(error => console.error(error));
};
