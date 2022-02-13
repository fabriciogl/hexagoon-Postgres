/*
 * Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
 */

// function showResposta(id){
//     form = document.getElementById('form'+id);
//     selecionado = form['alternativaRadio'].value;
//     resposta = document.getElementById('resposta'+id).getAttribute('value')
//     if (resposta === selecionado){
//         document.getElementById('resultado'+id).textContent = 'Você acertou!';
//     } else {
//         document.getElementById('resultado'+id).textContent = 'Você errou! A resposta correta é ' + resposta;
//     }
//     return false
// }

// Sugestão do MDN fazer isso, para evitar problema de memória.
function showResposta(event){
    selecionado = event.target['alternativaRadio'].value;
    resposta = event.target.querySelector('span').getAttribute('value');
    if (resposta === selecionado){
        event.target.querySelector('p#resultado').textContent = 'Você acertou!';
    } else {
        event.target.querySelector('p#resultado').textContent = 'Você errou! A resposta correta é ' + resposta + '.';
    }
    event.preventDefault()
}

window.onload = function loadFormFunctions(){
    document.querySelectorAll('form').forEach(function(form){
        form.addEventListener('submit', showResposta, false)
    })
};