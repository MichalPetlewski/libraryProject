const daysValue = document.querySelector('#day-value');
const daysWrapper = document.querySelector('.days-wrapper')

let howManyDaysLeft = parseInt(daysValue.innerHTML);


if(howManyDaysLeft > 14){
    daysWrapper.classList.add('green');
    daysWrapper.classList.remove('red');
    daysWrapper.classList.remove('orange');
}
else if(howManyDaysLeft < 14 && howManyDaysLeft > 5){
    daysWrapper.classList.add('orange');
    daysWrapper.classList.remove('red');
    daysWrapper.classList.remove('green');
}

else{
    daysWrapper.classList.add('red');
    daysWrapper.classList.remove('green');
    daysWrapper.classList.remove('orange');
}


