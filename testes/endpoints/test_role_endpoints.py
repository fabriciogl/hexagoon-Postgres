#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from banco_dados.sql_alchemy.configuracao.data_schema import Role


class TestRoleEndpoints:

    token = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, load_data):

        TestRoleEndpoints.token = client.post(
            "/autenticacao",
            json={"email": "joao@hexsaturn.space", "senha": "segredodojoao"}
        ).json().get('token')

        response = client.get(
            "role/1",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('id') == 1
        assert response.json().get('sigla')
        assert response.json().get('descricao')

    @staticmethod
    def test_create(session: Session, client: TestClient, load_data):

        response = client.post(
            "role",
            json={"sigla": "pro", "descricao": "acesso de conta paga"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        nova_role = session.query(Role).where(Role.sigla == 'pro').first()
        TestRoleEndpoints.novo_id = nova_role.id

        assert response.status_code == 201
        assert response.json().get('id') == nova_role.id

    @staticmethod
    def test_update(session: Session, client: TestClient, load_data):
        response = client.put(
            f"role/{TestRoleEndpoints.novo_id}",
            json={"sigla": "paid"},
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        update_role = session.query(Role).where(Role.id == TestRoleEndpoints.novo_id).first()
        session.refresh(update_role)

        assert response.status_code == 200
        assert update_role.sigla == "paid"

    @staticmethod
    def test_delete(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"role/{TestRoleEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_role = session.query(Role).where(Role.id == TestRoleEndpoints.novo_id).first()

        assert response.status_code == 200
        assert delete_role.deletado_em is not None
        assert delete_role.deletado_por is not None

    @staticmethod
    def test_not_found(session: Session, client: TestClient, load_data):
        response = client.get(
            f"role/{TestRoleEndpoints.novo_id + 1}",
            headers={'Authorization': f'Bearer {TestRoleEndpoints.token}'}
        )

        assert response.status_code == 406