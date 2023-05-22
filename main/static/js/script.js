const sendAjaxRequest = (method, url, body = null) => {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const headers = {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/x-www-form-urlencoded'
    };
        return fetch(url, { method, headers, body })
        .then(response => response.json())
        .catch(error => console.error(error));
};

const report = (type, id, reason) => {
    const url = '/report/';
    const method = 'POST';
    const body = `type=${encodeURIComponent(type)}&id=${encodeURIComponent(id)}&reason=${encodeURIComponent(reason)}`;
    sendAjaxRequest(method, url, body);
};
  
