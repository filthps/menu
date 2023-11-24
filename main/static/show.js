function show_first_ahead_current() {
// 2) Все, что над выделенным пунктом - развернуто
    var current = document.getElementsByClassName("current");
    var current = current.length ? current[0] : null;
    var prev = current.parentNode || null;
    while (prev && prev.className != "main") {
        prev.classList.remove("hidden");
        var prev = prev.parentElement;
    }
};
show_first_ahead_current();
