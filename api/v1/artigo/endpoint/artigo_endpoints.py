#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from fastapi import APIRouter
from fastapi.params import Security

from api.v1.artigo.acoes.artigo_acoes import ArtigoAcoes
from api.v1.artigo.model.artigo_model import ArtigoOut, ArtigoIn
from api.v1.artigo.regras.artigo_regras import ArtigoRegras
from api.v1.recursos.response_handler import ResponseHandler
from api.v1.recursos.validations.token_role_validation import valida_role

router = APIRouter(
    prefix="/artigo",
    tags=['Artigo']
)


class ArtigoEndpoints:

    @staticmethod
    @router.get(
        "/{_id}",
        response_model=ArtigoOut
    )
    def find(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # valida as regras necessárias no model

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, handler=handler, acao='find')

        return handler.sucesso

    # O response_model_exclude funciona somente para a sucesso do request, mas não para a documentação
    @staticmethod
    @router.post(
        "",
        response_model=ArtigoOut,
        status_code=201
    )
    async def create(
            model: ArtigoIn,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ArtigoAcoes(model=model, handler=handler, acao='create')

        return handler.sucesso

    @staticmethod
    @router.put(
        "/{_id}",
        status_code=200,
        response_model=ArtigoOut
    )
    async def update(
            model: ArtigoIn,
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["user"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(_id=_id, model=model, handler=handler, regra='update')

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, model=model, handler=handler, acao='update')

        return handler.sucesso

    @staticmethod
    @router.delete(
        "/{_id}",
        status_code=200
    )
    async def delete(
            _id: int,
            handler: ResponseHandler = Security(valida_role, scopes=["admin"])
    ):
        # regras aplicáveis ao model
        ArtigoRegras(_id=_id, handler=handler, regra='softdelete')

        # realiza as acoes necessárias no model
        ArtigoAcoes(_id=_id, handler=handler, acao='softdelete')

        return handler.sucesso
