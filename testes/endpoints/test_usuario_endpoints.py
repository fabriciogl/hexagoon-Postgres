#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from banco_dados.sql_alchemy.configuracao.data_schema import Usuario


class TestUsuarioEndpoint:

    token = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, load_data):

        TestUsuarioEndpoint.token = client.post(
            "/autenticacao",
            json={"email": "joao@hexsaturn.space", "senha": "segredodojoao"}
        ).json().get('token')

        response = client.get(
            "usuario/1",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('id') == 1
        assert response.json().get('a_roles')[0]['role']['sigla'] == 'root'

    @staticmethod
    def test_create(session: Session, client: TestClient, load_data):

        response = client.post(
            "usuario",
            json={"nome": "Erick Hobsbawn", "email": "eric@hexsaturn.space", "senha": "extremo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        novo_usuario = session.query(Usuario).where(Usuario.email == 'eric@hexsaturn.space').first()
        TestUsuarioEndpoint.novo_id = novo_usuario.id

        assert response.status_code == 201
        assert response.json().get('id') == novo_usuario.id
        assert response.json().get('a_roles') == []

    @staticmethod
    def test_update(session: Session, client: TestClient, load_data):
        response = client.put(
            "usuario/1",
            json={"nome": "João do Pulo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        update_usuario = session.query(Usuario).where(Usuario.id == 1).first()
        session.refresh(update_usuario)

        assert response.status_code == 200
        assert update_usuario.nome == "João do Pulo"

    @staticmethod
    def test_inactivate(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id}/inactivate",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        inactivate_usuario = session.query(Usuario).where(Usuario.id == TestUsuarioEndpoint.novo_id).first()

        assert response.status_code == 200
        assert inactivate_usuario.ativo == False
        assert response.json().get('resultado') == 'usuário inativado.'

    @staticmethod
    def test_delete(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_usuario = session.query(Usuario).where(Usuario.id == TestUsuarioEndpoint.novo_id).first()

        assert response.status_code == 200
        assert delete_usuario.deletado_em is not None
        assert delete_usuario.deletado_por is not None

    @staticmethod
    def test_usuario_not_found(session: Session, client: TestClient, load_data):
        response = client.get(
            f"usuario/{TestUsuarioEndpoint.novo_id + 1}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_update_email(session: Session, client: TestClient, load_data):
        response = client.put(
            "usuario/1",
            json={"email": "joao@hexjupiter.space"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        update_usuario = session.query(Usuario).where(Usuario.id == 1).first()
        session.refresh(update_usuario)

        assert response.status_code == 422
        assert update_usuario.email == "joao@hexsaturn.space"

    @staticmethod
    def test_create_email_utilizado(session: Session, client: TestClient, load_data):

        response = client.post(
            "usuario",
            json={"nome": "Erick Hobsbawn", "email": "eric@hexsaturn.space", "senha": "extremo"},
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 422


    @staticmethod
    def test__delete(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"usuario/{TestUsuarioEndpoint.novo_id + 1}",
            headers={'Authorization': f'Bearer {TestUsuarioEndpoint.token}'}
        )

        assert response.status_code == 406