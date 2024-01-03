const words = document.querySelectorAll('.word');
const definitions = document.querySelectorAll('.definition');

function applyBlurEffect(selected) {
    if (selected.id === 'blurWords') {
        words.forEach(word => word.classList.add('blur-effect'));
        definitions.forEach(definition => definition.classList.remove('blur-effect'));
    } else if (selected.id === 'neutral') {
        words.forEach(word => word.classList.remove('blur-effect'));
        definitions.forEach(definition => definition.classList.remove('blur-effect'));
    } else if (selected.id === 'blurDefinitions') {
        words.forEach(word => word.classList.remove('blur-effect'));
        definitions.forEach(definition => definition.classList.add('blur-effect'));
    }
    updateURLParams(selected.id);
    updateLinks(selected.id);
}

function handleRadioButtonChange() {
    const selected = document.querySelector('input[name="switch"]:checked');
    applyBlurEffect(selected);
}

function updateLinks(selectedID) {
    document.querySelectorAll('a[href*="/en/view"], a[href*="/en/rand"]').forEach(link => {
        const href = link.getAttribute('href');
        const regex = /selected=[^&]+/;
        if (regex.test(href)) {
            link.setAttribute('href', href.replace(regex, 'selected=' + selectedID));
        } else {
            link.setAttribute('href', href + (href.includes('?') ? '&' : '?') + 'selected=' + selectedID);
        }
    });
}

function updateURLParams(selectedID) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('selected', selectedID);
    const newURL = `${window.location.pathname}?${urlParams.toString()}`;
    window.history.replaceState({}, '', newURL);
}

function retrieveURLParams() {
    const urlParams = new URLSearchParams(window.location.search);
    const selectedID = urlParams.get('selected');
    if (selectedID) {
        const selected = document.getElementById(selectedID);
        if (selected) {
            selected.checked = true;
            applyBlurEffect(selected);
        }
    }
}

document.querySelectorAll('.toggle-input').forEach(radio => {
    radio.addEventListener('change', handleRadioButtonChange);
});

retrieveURLParams();