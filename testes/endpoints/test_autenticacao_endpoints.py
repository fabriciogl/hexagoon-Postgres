#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.testclient import TestClient


class TestAutenticacao:

    # é necessário importar o load_data a cada requisição
    # se quiser que as informações que ele gerou
    @staticmethod
    def test_token_sucesso(client: TestClient, load_data):

        response = client.post(
            "/autenticacao",
            json={"email": "joao@hexsaturn.space", "senha": "segredodojoao"}
        )

        assert response.json().get('token')
        assert response.json().get('exp')
        assert response.json().get('roles')

    @staticmethod
    def test_user_inativo(client: TestClient, load_data):
        response = client.post(
            "/autenticacao",
            json={"email": "brenda@hexsaturn.space", "senha": "maionese"}
        )
        assert response.json().get('detail')
        assert response.status_code == 401

    @staticmethod
    def test_senha_incorreta(client: TestClient, load_data):
        response = client.post(
            "/autenticacao",
            json={"email": "fabricio@hexsaturn.space", "senha": "bolinho"}
        )
        assert response.json().get('detail')
        assert response.status_code == 401

    @staticmethod
    def test_token_usuario_inexistente(client: TestClient, load_data):
        response = client.post(
            "/autenticacao",
            json={"email": "jorbas@hexsaturn.space", "senha": "extremo"}
        )
        assert response.json().get('detail')
        assert response.status_code == 401

    @staticmethod
    def test_recupera_usuario(client: TestClient, load_data):
        response = client.post(
            "autenticacao/recuperar",
            json={"email": "maria@hexsaturn.space", "senha": "segredodamaria"}
        )
        assert response.status_code == 202

    @staticmethod
    def test_recuperar_usuario_inexistente(client: TestClient, load_data):
        response = client.post(
            "autenticacao/recuperar",
            json={"email": "jorbas@hexsaturn.space", "senha": "extremo"}
        )
        assert response.json().get('detail')
        assert response.status_code == 406
