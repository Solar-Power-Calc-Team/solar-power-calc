import { get_page_storage } from "./utils.js";

const name = get_page_storage("name");

const title = document.querySelector("title");
const welcome = document.querySelector(".welcome_message");

title.textContent.replace("%s", name);
welcome.textContent.replace("%s", name);

window.setTimeout(() => {
    const calculated = get_page_storage("calculated");
    if (calculated == "yes") {
        window.location.href = "./calc_result.html"
    } else {
        window.location.href = "./calc_house.html"
    }
}, 3);