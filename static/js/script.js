// Prevent accordion from closing on page refresh, doing this by assigning
// each accordion with a key and saving that using local storage
document.addEventListener('DOMContentLoaded', function () {
    let accordion = document.getElementById('accordionFlushExample');
    let collapseElements = accordion.querySelectorAll('.accordion-collapse');

    collapseElements.forEach(function (collapse) {
        let key = 'accordion:' + collapse.id;
        let data = localStorage.getItem(key);
        if (data === 'true') {
            collapse.classList.add('show');
        }
        collapse.addEventListener('show.bs.collapse', function () {
            localStorage.setItem(key, 'true');
        });
        collapse.addEventListener('hide.bs.collapse', function () {
            localStorage.setItem(key, 'false');
        });
    });
});

// Call the scrollToBottom function when the page finishes loading
function scrollToBottom() {
    let messagesContainer = document.querySelector('.room-messages-container');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


window.onload = function() {
    scrollToBottom();
};

// Display image before user uploads
function previewImage(event) {
    let reader = new FileReader();
    reader.onload = function() {
      let preview = document.getElementById('image-preview');
      preview.src = reader.result;
      preview.style.display = 'block';
    }
    reader.readAsDataURL(event.target.files[0]);
  }