#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from passlib.hash import bcrypt

from banco_dados.sql_alchemy.configuracao.data_schema import Usuario, Role, AsUsuarioRole, AsRolePrecedencia
from config import settings


def load_data(session):

    # cria usuário root
    role_root = Role(sigla='root', descricao='acesso com poder de superusuário')
    as_role_usuario = AsUsuarioRole()
    as_role_usuario.role = role_root
    usuario = Usuario(
        nome=settings.root_user,
        email=settings.root_email,
        senha=bcrypt.using(rounds=7).hash(settings.root_senha),
        ativo=True
    )
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


    session.commit()

