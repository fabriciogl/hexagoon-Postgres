#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi.params import Depends
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.v1.recursos.basic_exceptions.login_exceptions import LoginException
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.usuario.model.usuario_model import UsuarioTokenIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario, SQLSincrono


async def check_password(
        request: Request,
        usuario_model: UsuarioTokenIn,
        session: Session = Depends(SQLSincrono.create_session)
) -> ResponseHandler:
    # busca o usuário no banco de dados
    select_query = select(Usuario) \
        .where(Usuario.email == usuario_model.email)
    try:
        usuario_data: Usuario = session.execute(select_query).scalar_one()

    except NoResultFound:
        raise LoginException(ordem=1, usuario=usuario_model, request=request)

    if not usuario_data.ativo:
        raise LoginException(ordem=2, usuario=usuario_model, request=request)

    if bcrypt.verify(usuario_model.senha, usuario_data.senha) is False:
        raise LoginException(ordem=3, usuario=usuario_model, request=request)

    # cria o handler da requisicao
    handler = ResponseHandler()
    handler.usuario = usuario_data
    handler.sessao = session
    handler.request = request

    return handler
