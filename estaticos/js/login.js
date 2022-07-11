/*
 * Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
 */

async function logarUsuario(){

    const email = document.querySelector('#email').value;
    const senha = document.querySelector('#senha').value;

    const login_response = await fetch(`http://0.0.0.0:8000/hexagoon/administration`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "email": email,
            "senha": senha
        })
    });

    if (!login_response.ok) {
        const resposta = await login_response.json();
        const p = document.createElement("p");
        const alerta = document.createTextNode(`Falha na autenticação! ${resposta['detail']}`);
        p.appendChild(alerta); //adiciona o nó de texto à nova div criada
        document.querySelector('#navigation').appendChild(p);
    }

    if (login_response.ok){

        // acessa o header
        const header = login_response.headers;
        const jwt = header.get('authorization');

        // setar o jwt no localstorage
        localStorage.setItem("jwt", jwt);

        // tentei setar o token no header de resposta, mas ele não integra o header de request
        // window.location.assign(resultado)


        // // rederiza a resposta da api/hexagoon/administration
        const resposta = await login_response.text();
        document.write(resposta);

        window.history.pushState('', '', 'administration');
    }
}