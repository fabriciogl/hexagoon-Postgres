#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from banco_dados.sql_alchemy.configuracao.data_schema import AsUsuarioRole, AsRolePrecedencia


class TestAsRolePrecedenciaEndpoints:

    token = None
    novo_id = None

    @staticmethod
    def test_find(client: TestClient, load_data):

        TestAsRolePrecedenciaEndpoints.token = client.post(
            "/autenticacao",
            json={"email": "joao@hexsaturn.space", "senha": "segredodojoao"}
        ).json().get('token')

        response = client.get(
            "as_role_precedencia/1",
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )
        assert response.status_code == 200
        assert response.json().get('id')
        assert response.json().get('precedencia')
        assert response.json().get('sub_role')
        assert response.json().get('criado_em')

    @staticmethod
    def test_create(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_role_precedencia",
            json={"sub_role_id": 2, "precedencia_id": 3},
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )

        nova_as_role_precedencia = session.query(AsRolePrecedencia)\
            .where(AsRolePrecedencia.id == response.json().get('id'))\
            .first()
        TestAsRolePrecedenciaEndpoints.novo_id = nova_as_role_precedencia.id

        assert response.status_code == 201
        assert response.json().get('precedencia').get('id') == 3
        assert response.json().get('sub_role').get('id') == 2

    @staticmethod
    def test_update(session: Session, client: TestClient, load_data):
        response = client.put(
            f"as_role_precedencia/{TestAsRolePrecedenciaEndpoints.novo_id}",
            json={"sub_role_id": 3},
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )

        update_role = session.query(AsRolePrecedencia).where(AsRolePrecedencia.id == TestAsRolePrecedenciaEndpoints.novo_id).first()
        session.refresh(update_role)

        assert response.status_code == 200
        assert update_role.sub_role_id == 3

    @staticmethod
    def test_delete(session: Session, client: TestClient, load_data):
        response = client.delete(
            f"as_role_precedencia/{TestAsRolePrecedenciaEndpoints.novo_id}",
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )

        # A query feita pelo teste não executa o listener do orm
        delete_role = session.query(AsRolePrecedencia).where(AsRolePrecedencia.id == TestAsRolePrecedenciaEndpoints.novo_id).first()

        assert response.status_code == 200
        assert delete_role.deletado_em is not None
        assert delete_role.deletado_por is not None

    @staticmethod
    def test_not_found(session: Session, client: TestClient, load_data):
        response = client.get(
            f"as_usuario_role/{TestAsRolePrecedenciaEndpoints.novo_id + 1}",
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )

        assert response.status_code == 406


    @staticmethod
    def test_create_no_role(session: Session, client: TestClient, load_data):

        response = client.post(
            "as_role_precedencia",
            json={"sub_role_id": 20, "precedencia_id": 2},
            headers={'Authorization': f'Bearer {TestAsRolePrecedenciaEndpoints.token}'}
        )

        assert response.status_code == 406
