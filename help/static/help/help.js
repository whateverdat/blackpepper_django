// Help App
addEventListener('DOMContentLoaded', () => {

    // Handle button toggles
    document.querySelectorAll('.nav-btn').forEach(button => {
        button.addEventListener('click', () => {
            let section = button.id.replace(/(-btn$)/, '');
            document.querySelectorAll('.nav-btn').forEach(button => {button.classList.remove('contrast')});
            document.querySelectorAll('.section').forEach(section => {section.classList.add('hidden')});
            document.querySelector(`#${section}`).classList.remove('hidden');
            button.classList.add('contrast');
        });
    });
    
    // Search
    document.querySelector('#query').addEventListener('input', () => {
        
        // Hide other divs and show manuel, then handle nav buttons
        document.querySelectorAll('.section').forEach(section => {section.classList.add('hidden')});
        document.querySelector('#app-manuel').classList.remove('hidden');
        document.querySelectorAll('.nav-btn').forEach(button => {button.classList.remove('contrast')});
        document.querySelector('#app-manuel-btn').classList.add('contrast');
        
        // Dynamically hide and show divs, depending on query
        const totalDivCount = document.querySelectorAll('.title').length;
        let hiddenDivCount = 0;
        let query = document.querySelector('#query').value;
        document.querySelectorAll('.title').forEach(title => {
            if (!title.children[0].innerHTML.includes(query.toUpperCase())) {
                title.classList.add('hidden');
                hiddenDivCount += 1;
            } else {
                title.classList.remove('hidden');
                hiddenDivCount -= 1;
            }
            if (hiddenDivCount === totalDivCount) {
                document.querySelector('.no-match').classList.remove('hidden');
            } else {
                document.querySelector('.no-match').classList.add('hidden');
            };
        });

        // Remove unmacthing headers
        document.querySelectorAll('.header').forEach(header => {
            let hide = true;
            for (let x of Array.from(header.children)) {
                if (!x.classList.contains('hidden'))
                hide = false;
            }
            if (hide === true) {
                header.classList.add('hidden');
            } else {
                header.classList.remove('hidden');
            };
        });
    });

    // Moify form
    document.querySelector('#id_request')[0].remove();
    
    
});