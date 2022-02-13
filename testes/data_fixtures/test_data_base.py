#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from banco_dados.sql_alchemy.configuracao.data_schema import AsRolePrecedencia, AsUsuarioRole, Artigo, Usuario, Role


def test_usuario(load_data):
    # insercao de usuário
    assert len(load_data.query(Usuario).all()) == 2

    # usuário ativos
    select_query = select(Usuario).where((Usuario.id == 1) & (Usuario.ativo == True))
    usuario = load_data.execute(select_query).scalar_one()
    assert len(usuario.a_roles) == 1


def test_role(load_data):
    assert len(load_data.query(Role).all()) == 3


def test_as_usuario_role(load_data):
    assert len(load_data.query(AsUsuarioRole).all()) == 1


def test_as_role_precedencia(load_data):
    assert len(load_data.query(AsRolePrecedencia).all()) == 3


def test_artigos(load_data):
    assert len(load_data.query(Artigo).all()) == 3
