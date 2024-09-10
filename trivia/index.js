const ANSWERS = {
    'question1': 'oreo',
    'question2': 'tideman'
}

const refs = {
    question1: document.getElementById('question-1'),
    question2: document.getElementById('question-2')
}

const resultElement = document.createElement('p');

refs.question1.addEventListener('change', (event) => {
    Array.from(refs.question1.elements).forEach((element) => {
        element.classList.remove('correct');
        element.classList.remove('incorrect');
    })
    if (event.target.value !== ANSWERS['question1']) {
        event.target.classList.add('incorrect');
        resultElement.textContent = 'Incorrect';
    } else {
        event.target.classList.add('correct');
        resultElement.textContent = 'Correct';
    }
    event.target.parentElement.appendChild(resultElement);
});

refs.question2.addEventListener('submit', (event) => {
    const inputValue = event.target.elements['problem-name'].value
    event.preventDefault();
    if (inputValue.toLowerCase() !== ANSWERS['question2']) {
        resultElement.textContent = 'Incorrect';
    } else {
        resultElement.textContent = 'Correct';
    }
    event.target.parentElement.appendChild(resultElement);
})
