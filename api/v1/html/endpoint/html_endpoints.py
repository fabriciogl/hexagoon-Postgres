#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from api.v1.html.acoes.html_acoes import HTMLAcoes
from api.v1.html.regras.html_regras import HTMLRegras
from api.v1.recursos.excecao_model import Message
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.password_validation import check_password
from banco_dados.sql_alchemy.configuracao.data_schema import SQLSincrono

router = APIRouter(
    prefix="/hexagoon",
    responses={404: {"model": Message}, 405: {"model": Message}, 401: {"model": Message}},
    tags=['HTML']
)


class HTMLEndpoints:

    @staticmethod
    @router.post(
        "/administration",
        response_class=HTMLResponse,
        status_code=200
    )
    async def admin_template(
            handler: ResponseHandler = Depends(check_password)
    ):
        # regras aplicáveis ao model
        HTMLRegras(handler=handler, regra='admin')

        # realiza as acoes necessárias no model
        HTMLAcoes(handler=handler, acao='admin')

        return handler.sucesso

    @staticmethod
    @router.get(
        "/login",
        response_class=HTMLResponse,
        status_code=200
    )
    async def login_template(request: Request):
        handler = ResponseHandler()
        handler.request = request

        # regras aplicáveis ao model
        HTMLRegras(handler=handler, regra='login')

        # realiza as acoes necessárias no model
        HTMLAcoes(handler=handler, acao='login')

        return handler.sucesso

    @staticmethod
    @router.get(
        "/artigos",
        response_class=HTMLResponse,
        status_code=200
    )
    async def articles_template(
            request: Request,
            session: Session = Depends(SQLSincrono.create_session)
    ):
        handler = ResponseHandler()
        handler.request = request
        handler.sessao = session

        # regras aplicáveis ao model
        HTMLRegras(handler=handler, regra='articleAll')

        # realiza as acoes necessárias no model
        HTMLAcoes(handler=handler, acao='articleAll')

        return handler.sucesso

    @staticmethod
    @router.get(
        "/artigo/{_id}",
        response_class=HTMLResponse,
        status_code=200
    )
    async def article_template(
            request: Request,
            _id: int,
            session: Session = Depends(SQLSincrono.create_session)
    ):
        handler = ResponseHandler()
        handler.request = request
        handler.sessao = session

        # regras aplicáveis ao model
        HTMLRegras(_id=_id, handler=handler, regra='article')

        # realiza as acoes necessárias no model
        HTMLAcoes(_id=_id, handler=handler, acao='article')

        return handler.sucesso
