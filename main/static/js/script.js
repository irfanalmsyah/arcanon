const sendAjaxRequest = (method, url, headers = {}, body = null) => {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    headers['X-CSRFToken'] = csrfToken;
        return fetch(url, { method, headers, body })
        .then(response => response.json())
        .catch(error => console.error(error));
};

const report = (type, id) => {
    const url = '/report/';
    const method = 'POST';
    const body = `type=${encodeURIComponent(type)}&id=${encodeURIComponent(id)}`;
    sendAjaxRequest(method, url, headers, body);
  };
  
