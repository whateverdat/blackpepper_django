// Dark Mode https://www.youtube.com/watch?v=wodWDIdV9BY&ab_channel=KevinPowell
addEventListener('DOMContentLoaded', () => {

    darkMode = localStorage.getItem("darkMode");
    const darkModeToggle = document.querySelector("#dark-mode-toggle");
    const html = document.querySelector("html");

    const enableDarkMode = () => {

        // Alter style
        html.setAttribute("data-theme", "dark");
        darkModeToggle.innerHTML = '<i id="theme-icon" class="fa-regular fa-lightbulb"></i>';

        // Store selection
        localStorage.setItem("darkMode", "enabled")
    }
    const disableDarkMode = () => {

        // Alter style
        html.setAttribute("data-theme", "light");
        darkModeToggle.innerHTML = '<i class="fa-solid fa-lightbulb"></i>';

        // Store selection
        localStorage.removeItem("darkMode")
    }

    if (!darkMode) {
        disableDarkMode();
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", () => {
            darkMode = localStorage.getItem("darkMode");
            if (darkMode !== 'enabled') {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        });
    }
})
    