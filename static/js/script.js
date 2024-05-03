// Prevent accordion from closing on page refresh, doing this by assigning
// each accordion with a key and saving that using local storage
document.addEventListener('DOMContentLoaded', function () {
    var accordion = document.getElementById('accordionFlushExample');
    var collapseElements = accordion.querySelectorAll('.accordion-collapse');

    collapseElements.forEach(function (collapse) {
        var key = 'accordion:' + collapse.id;
        var data = localStorage.getItem(key);
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