#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from banco_dados.sql_alchemy.configuracao.data_schema import AsUsuarioRole


class TestAsUsuarioRoleEndpoints:

    token = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, load_data):

        TestAsUsuarioRoleEndpoints.token = client.post(
            "/autenticacao",
            json={"email": "joao@hexsaturn.space", "senha": "segredodojoao"}
        ).json().get('token')

        response = client.get(
            "as_usuario_role/1",
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('id')
        assert response.json().get('usuario')
        assert response.json().get('role')
        assert response.json().get('criado_em')

    @staticmethod
    def test_create(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_usuario_role",
            json={"usuario_id": 2, "role_id": 2},
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        nova_as_usuario_role = session.query(AsUsuarioRole)\
            .where(AsUsuarioRole.id == response.json().get('id'))\
            .first()
        TestAsUsuarioRoleEndpoints.novo_id = nova_as_usuario_role.id

        assert response.status_code == 201
        assert response.json().get('usuario').get('id') == 2
        assert response.json().get('role').get('id') == 2

    @staticmethod
    def test_update(session: Session, client: TestClient, load_data):
        response = client.put(
            f"as_usuario_role/{TestAsUsuarioRoleEndpoints.novo_id}",
            json={"role_id": 3},
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        update_role = session.query(AsUsuarioRole).where(AsUsuarioRole.id == TestAsUsuarioRoleEndpoints.novo_id).first()
        session.refresh(update_role)

        assert response.status_code == 200
        assert update_role.role_id == 3

    @staticmethod
    def test_delete(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"as_usuario_role/{TestAsUsuarioRoleEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_role = session.query(AsUsuarioRole).where(AsUsuarioRole.id == TestAsUsuarioRoleEndpoints.novo_id).first()

        assert response.status_code == 200
        assert delete_role.deletado_em is not None
        assert delete_role.deletado_por is not None

    @staticmethod
    def test_not_found(session: Session, client: TestClient, load_data):
        response = client.get(
            f"as_usuario_role/{TestAsUsuarioRoleEndpoints.novo_id + 1}",
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        assert response.status_code == 406


    @staticmethod
    def test_create_no_user(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_usuario_role",
            json={"usuario_id": 20, "role_id": 2},
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_create_no_role(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_usuario_role",
            json={"usuario_id": 2, "role_id": 20},
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        assert response.status_code == 406

    @staticmethod
    def test_create_role_existente(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_usuario_role",
            json={"usuario_id": 1, "role_id": 1},
            headers={'Authorization': f'Bearer {TestAsUsuarioRoleEndpoints.token}'}
        )

        assert response.status_code == 422
