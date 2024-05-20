const form = document.querySelector('#form');
const button = document.querySelector('.submit-button');

console.log('laduje');

button.addEventListener('click', reloadForm);


function reloadForm(){
    console.log('dupa');
    form.submit();
};