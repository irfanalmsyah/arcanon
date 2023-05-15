const sendAjaxRequest = (method, url, headers = {}, body = null) => {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    headers['content-type'] = 'aapplication/x-www-form-urlencoded';
    headers['X-CSRFToken'] = csrfToken;
        return fetch(url, { method, headers, body })
        .then(response => response.json())
        .catch(error => console.error(error));
};

const report = (type, id) => {
    const url = '/report/';
    const method = 'POST';
    const body = `type=${encodeURIComponent(type)}&id=${encodeURIComponent(id)}`;
    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    };
    sendAjaxRequest(method, url, headers, body);
  };
  
