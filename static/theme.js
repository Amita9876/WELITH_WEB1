
document.addEventListener("DOMContentLoaded", function () {

    const themeToggle = document.getElementById("themeToggle");
    const body = document.body;

    // Check saved theme in localStorage
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
    }

    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener("click", function () {

            body.classList.toggle("dark-mode");

            // Save theme in localStorage
            if (body.classList.contains("dark-mode")) {
                localStorage.setItem("theme", "dark");
            } else {
                localStorage.setItem("theme", "light");
            }
        });
    }

});