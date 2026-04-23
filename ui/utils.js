function to_data_header(method) {
    return {
        method: method,
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        }
    };
}

export async function send_put(json_data) {
    const location = window.location.protocol + "//" + window.location.host;
    const header = {
        ...to_data_header("PUT"),
        body: JSON.stringify(json_data)
    };

    try {
        return await fetch(location, header);
    } catch (e) {
        alert("We failed to get a proper response from the server. Check the console log for more information. We apologise for the inconvenience.");
        console.error("ERROR: Failed to send GET request: " + e);
        throw e; // Bruh 💀🥀🥀
    }
}

export async function send_get(json_data) {
    const location = window.location.protocol + "//" + window.location.host;
    const header = {
        ...to_data_header("GET"),
        body: JSON.stringify(json_data)
    }

    try {
        return await fetch(location, header);
    } catch (e) {
        alert("We failed to get a proper response from the server. Check the console log for more information. We apologise for the inconvenience.");
        console.error("ERROR: Failed to send GET request: " + e);
        throw e; // Bruh 💀🥀🥀
    }   
}

export function assert(_eval, fn) {
    if (!_eval) {
        throw new Error(fn + "() | " + _eval.toString() + " failed");
    }
}

export function set_page_storage(key, value) {
    assert(key !== null && value !== null, "set_page_storage");
    assert(typeof key === "string", "set_page_storage");
    window.sessionStorage.setItem(key, JSON.stringify(value));
}

export function get_page_storage(key) {
    assert(key !== null && value !== null, "get_page_storage");
    assert(typeof key === "string", "get_page_storage");
    const val =  window.sessionStorage.getItem(key);
    return JSON.parse(val);
}