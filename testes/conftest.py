#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json
from typing import Generator

import pytest
from passlib.hash import bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from starlette.testclient import TestClient

from banco_dados.sql_alchemy.configuracao.data_schema import SQLSincrono, Base, Usuario, Role, AsUsuarioRole, \
    AsRolePrecedencia, Artigo
from main import app


@pytest.fixture(scope="package")
def setup_db():
    engine = SQLSincrono.create_engine()

    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)

    # cria um banco de dados caso não exista
    Base.metadata.create_all(bind=SQLSincrono.engine)

    yield SQLSincrono.create_session()


@pytest.fixture(scope="package")
def load_data(setup_db):
    session = setup_db.__next__()

    # Creates user
    usuario = Usuario(nome='João da Silva', email='joao@hexsaturn.space', ativo=True)
    usuario2 = Usuario(nome='Maria da Silva', email='maria@hexsaturn.space', ativo=False)
    usuario.senha = bcrypt.using(rounds=7).hash('segredodojoao')
    usuario2.senha = bcrypt.using(rounds=7).hash('segredodamaria')
    session.add(usuario)
    session.add(usuario2)
    role_root = Role(sigla='root', descricao='acesso com poder de superusuário')
    as_role_usuario = AsUsuarioRole()
    as_role_usuario.role = role_root
    usuario.a_roles.append(as_role_usuario)
    session.add(usuario)

    # cria demais roles
    role_admin = Role(sigla='admin', descricao='acesso com poder de administração')
    role_user = Role(sigla='user', descricao='acesso com poder de usuário')
    session.add_all([role_admin, role_user])

    # cria as precedencias
    as_role_precedencia_1 = AsRolePrecedencia(sub_role=role_admin, precedencia=role_root)
    as_role_precedencia_2 = AsRolePrecedencia(sub_role=role_user, precedencia=role_root)
    as_role_precedencia_3 = AsRolePrecedencia(sub_role=role_user, precedencia=role_admin)
    session.add_all([as_role_precedencia_1, as_role_precedencia_2, as_role_precedencia_3])
    # Creates artigos
    artigo1 = Artigo(titulo='Dança dos Lobos',
                     corpo=json.dumps('Dançar com um lobo pode ser a última dança ta tua vida.'))
    artigo2 = Artigo(titulo='Dança dos Gatos', corpo=json.dumps('Dançar com um gato pode ser arriscado.'))
    artigo3 = Artigo(titulo='Dança dos Coelhos', corpo=json.dumps('Dançar com um coelho pode ser interessante.'))
    session.add_all([artigo1, artigo2, artigo3])
    session.commit()

    yield session


@pytest.fixture(scope="function")
def session(load_data):

    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=SQLSincrono.engine.connect()  # Por abrir uma conexão por sessão, também tem que fechar ao final.
    )

    session = Session()
    try:

        yield session

    # o finally será executado somente após a resposta da requisicao
    finally:
        # fechar a sessão não fecha a conexão automaticamente,
        # tem que fazer as duas manualmente.
        session.bind.connection.close()
        session.close()


@pytest.fixture(scope="package")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
