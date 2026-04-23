function register_click(classname, location) {
    document.querySelector(`.${classname}`).addEventListener('click', function() { window.location.href = `./${location}` })
}

register_click("header_logo", "index.html")

if (window.location.href.includes("index.html")) {
    register_click("index_login", "login.html")
    register_click("index_signup", "signup.html")
}