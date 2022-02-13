#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.v1.autenticacao.acoes.autenticacao_acoes import AutenticacaoAcoes
from api.v1.autenticacao.model.autenticacao_model import AutenticacaoOut
from api.v1.autenticacao.regras.autenticacao_regras import AutenticacaoRegras
from api.v1.recursos.excecao_model import Message
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.password_validation import check_password
from api.v1.usuario.model.usuario_model import UsuarioTokenIn
from banco_dados.sql_alchemy.configuracao.data_schema import SQLSincrono

router = APIRouter(
    prefix="/autenticacao",
    responses={401: {"model": Message}, 404: {"model": Message}, 405: {"model": Message}, 406: {"model": Message}},
    tags=['Auth']
)


class AutenticacaoEndpoints:

    @staticmethod
    @router.post("",
                 response_model=AutenticacaoOut,
                 status_code=201)
    def create_token(
            handler: ResponseHandler = Depends(check_password)
    ):
        AutenticacaoRegras(model=handler.usuario, handler=handler, regra='login')

        AutenticacaoAcoes(model=handler.usuario, handler=handler, acao='login')

        return handler.sucesso



    @staticmethod
    @router.post("/recuperar",
                 response_class=JSONResponse,
                 status_code=202)
    async def recupera_conta(
            request: Request,
            model: UsuarioTokenIn,
            sessao: Session = Depends(SQLSincrono.create_session)
    ):
        handler = ResponseHandler(session=sessao)
        handler.request = request
        request.state._state['handler'] = handler

        AutenticacaoRegras(model=model, handler=handler, regra='recuperar')

        AutenticacaoAcoes(model=model, handler=handler, acao='recuperar')

        return handler.sucesso
