#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.as_role_precedencia.model.as_role_precedencia import AsRolePrecedenciaOut, AsRolePrecedenciaIn
from api.v1.as_role_precedencia.acoes.as_role_precedencia import AsRolePrecedenciaAcoes
from api.v1.as_role_precedencia.regras.as_role_precedencias import AsRolePrecedenciaRegras
from api.v1.as_usuario_role.regras.as_usuario_role_regras import AsUsuarioRoleRegras
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/as_role_precedencia",
    tags=['Associação Role Precedencia']
)


class AsRolePrecedenciaEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=AsRolePrecedenciaOut
    )
    async def find(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsRolePrecedenciaRegras(_id=_id, handler=handler, regra='find')
        # realiza as acoes necessárias no model
        AsRolePrecedenciaAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=AsRolePrecedenciaOut,
        status_code=201
    )
    async def create(
            model: AsRolePrecedenciaIn,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsRolePrecedenciaRegras(model=model, handler=handler, regra='create')
        # realiza as acoes necessárias no model
        AsRolePrecedenciaAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=AsRolePrecedenciaOut
    )
    async def update(
            model: AsRolePrecedenciaIn,
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["root", "admin"])
    ):
        # valida as regras necessárias no model
        AsRolePrecedenciaRegras(model=model, _id=_id, handler=handler, regra='update')
        # realiza as acoes necessárias no model
        AsRolePrecedenciaAcoes(model=model, _id=_id, handler=handler, acao='update')

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
        AsRolePrecedenciaRegras(_id=_id, handler=handler, regra='softdelete')
        # realiza as acoes necessárias no model
        AsRolePrecedenciaAcoes(_id=_id, handler=handler, acao='softdelete')

        return handler.sucesso
