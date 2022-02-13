/*
 * Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
 */

async function excluirUsuario(id){

    const token = localStorage.getItem("jwt");

    const response = await fetch(`http://0.0.0.0:8000/usuario/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const message = `Um erro ocorreu ${response.status}`;
        throw new Error(message);
    }
    if (response.status === 200){
        const nome = document.querySelector(`#u${id}`)
        nome.style.textDecoration = 'line-through';
    }

}

async function desativarUsuario(id){

    const token = localStorage.getItem("jwt");

    const response = await fetch(`https://hexagoon-ev3arw55ca-ue.a.run.app/usuario/${id}/inactivate`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const message = `Um erro ocorreu ${response.status}`;
        throw new Error(message);
    }
    if (response.status === 200){
        const nome = document.querySelector(`#ua${id}`)
        nome.textContent = 'Não';
    }

}

async function ativarUsuario(id) {

    const token = localStorage.getItem("jwt");

    const email = document.querySelector(`#e${id}`).innerText;

    const response = await fetch(`https://hexagoon-ev3arw55ca-ue.a.run.app/autenticacao/recuperar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            "email": email
        })
    });

    if (!response.ok) {
        const message = `Um erro ocorreu ${response.status}`;
        throw new Error(message);
    }
    if (response.status === 202) {
        const nome = document.querySelector(`#ua${id}`);
        nome.textContent = 'Sim';
    }
}

async function showFormUsuario(){
        const form = document.querySelector('#criaUsuario');
        form.style.display = 'table';
}

async function submeterUsuario(){

    const token = localStorage.getItem("jwt");

    const email = document.querySelector('#email').value;
    const senha = document.querySelector('#senha').value;
    const nome = document.querySelector('#nome').value;

    const create_response = await fetch(`https://hexagoon-ev3arw55ca-ue.a.run.app/usuario`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            "email": email,
            "senha": senha,
            "nome": nome
        })
    });

    if (!create_response.ok) {
        const resposta = await create_response.json();
        const p = document.createElement("p");
        const alerta = document.createTextNode(`Falha na autenticação! ${resposta['detail']}`);
        p.appendChild(alerta); //adiciona o nó de texto à nova div criada
        document.querySelector('#criaUsuario').appendChild(p);
    }

    if (create_response.status === 201) {
        const resposta = await create_response.json();
        const p = document.createElement("p");
        const alerta = document.createTextNode(`Usuário id ${resposta['id']} criado com sucesso`);

        const user_layout = document.querySelector('table[layout=usuario]');
        const user_clone = user_layout.cloneNode(true);
        let id = user_clone.querySelector('table  tr:first-child td:nth-child(2)').getAttribute('id');
        id = id.replace('u', '');
        user_clone.querySelector(`#u${id}`).innerText = resposta['nome'];
        user_clone.querySelector(`#u${id}`).setAttribute('id', `u${resposta['id']}`);
        user_clone.querySelector(`#e${id}`).innerText = resposta['email'];
        user_clone.querySelector(`#e${id}`).setAttribute('id', `e${resposta['id']}`);
        user_clone.querySelector(`#ua${id}`).innerText = 'Sim';
        user_clone.querySelector(`#ua${id}`).setAttribute('id', `ua${resposta['id']}`);
        document.querySelector('#navigation').appendChild(user_clone);
    }
}
