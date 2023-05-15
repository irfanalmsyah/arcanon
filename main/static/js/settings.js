function openTabFromUrl() {
    var url = window.location.href;
    var hashIndex = url.indexOf("#");
    if (hashIndex !== -1) {
        var tabId = url.substring(hashIndex);
        var tab = document.querySelector('a[href="' + tabId + '"]');
        if (tab) {
            tab.click();
        }
    }
}

// Call the function when the page has finished loading
window.onload = openTabFromUrl

const profileImg = document.querySelector('.profile-img');
const input = profileImg.querySelector('#image');

profileImg.addEventListener('click', () => {
    input.click();
});

input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', () => {
            profileImg.querySelector('img').setAttribute('src', reader.result);
        });
        reader.readAsDataURL(file);
    }
});

