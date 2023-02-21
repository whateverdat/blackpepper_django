addEventListener('DOMContentLoaded', () => {

    message = document.querySelector('#message');

    try {
        setTimeout(function(){
            message.remove();
        }, 5000);

        document.querySelector('#close-message').addEventListener('click', () => {
            message.remove()
        })
    } catch (TypeError) {
        // No flash message
    }

});