// Check url for image https://stackoverflow.com/questions/9714525/javascript-image-url-verify
function checkURL(url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}

export {checkURL};