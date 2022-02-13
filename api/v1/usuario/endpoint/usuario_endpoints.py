#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.recursos.excecao_model import Message
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.token_role_validation import valida_role
from api.v1.usuario.acoes.usuario_acoes import UsuarioAcoes
from api.v1.usuario.model.usuario_model import UsuarioIn, UsuarioOut
from api.v1.usuario.regras.usuario_regras import UsuarioRegras

router = APIRouter(
    prefix="/usuario",
    responses={404: {"model": Message}, 405: {"model": Message}, 401: {"model": Message}},
    tags=['Usuário']
)


class UsuarioEndpoints:

    @staticmethod
    @router.get("/{id}",
                response_model=UsuarioOut
                )
    async def find(
            id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # realiza as rules necessárias no model
        UsuarioRegras(_id=id, handler=handler, regra='find')
        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=id, handler=handler, acao='find')

        return handler.sucesso
    # O response_model_exclude funciona somente para a resposta do request, mas não para a documentação

    @staticmethod
    @router.post("",
                 response_model=UsuarioOut,
                 status_code=201)
    async def create(
            usuario: UsuarioIn,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        UsuarioRegras(model=usuario, handler=handler, regra='create')
        # realiza as acoes necessárias no model
        UsuarioAcoes(model=usuario, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put("/{_id}",
                response_model=UsuarioOut,
                status_code=200
                )
    async def update(
            usuario: UsuarioIn,
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, model=usuario, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, model=usuario, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200
    )
    async def delete(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, handler=handler, regra='softdelete')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, handler=handler, acao='softdelete')

    @staticmethod
    @router.delete(
        "/{_id}/inactivate",
        status_code=200
    )
    async def inactivate(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):

        # regras aplicáveis ao model
        UsuarioRegras(_id=_id, handler=handler, regra='inactivate')

        # realiza as acoes necessárias no model
        UsuarioAcoes(_id=_id, handler=handler, acao='inactivate')

        return handler.sucesso


