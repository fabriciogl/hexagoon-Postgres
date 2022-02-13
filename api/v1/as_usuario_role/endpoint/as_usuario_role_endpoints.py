#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.as_usuario_role.acoes.as_usuario_role_acoes import AsUsuarioRoleAcoes
from api.v1.as_usuario_role.model.as_usuario_role_model import AsUsuarioRoleOut, AsUsuarioRoleIn
from api.v1.as_usuario_role.regras.as_usuario_role_regras import AsUsuarioRoleRegras
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/as_usuario_role",
    tags=['Associação Usuário Role']
)


class AsUsuarioRoleEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=AsUsuarioRoleOut
    )
    async def find(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsUsuarioRoleRegras(_id=_id, handler=handler, regra='find')
        # realiza as acoes necessárias no model
        AsUsuarioRoleAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=AsUsuarioRoleOut,
        status_code=201
    )
    async def create(
            model: AsUsuarioRoleIn,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsUsuarioRoleRegras(model=model, handler=handler, regra='create')
        # realiza as acoes necessárias no model
        AsUsuarioRoleAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=AsUsuarioRoleOut
    )
    async def update(
            model: AsUsuarioRoleIn,
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsUsuarioRoleRegras(model=model, _id=_id, handler=handler, regra='update')
        # realiza as acoes necessárias no model
        AsUsuarioRoleAcoes(model=model, _id=_id, handler=handler, acao='update')

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
        # valida as regras necessárias no model
        AsUsuarioRoleRegras(_id=_id, handler=handler, regra='softdelete')
        # realiza as acoes necessárias no model
        AsUsuarioRoleAcoes(_id=_id, handler=handler, acao='softdelete')

        return handler.sucesso
