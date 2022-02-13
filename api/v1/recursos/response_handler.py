# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos
# reservados.
from typing import Optional, Any

from sqlalchemy.orm import Session
from starlette.requests import Request

from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario


class ResponseHandler:

    def __init__(self, session: Session = None):
        self._sessao: Optional[Session] = session
        self._request: Optional[Request] = None
        self._usuario: Optional[Usuario] = None
        self._sucesso: Optional[Any] = None
        self._acao: Optional[str] = None

    @property
    def sucesso(self):
        return self._sucesso

    @sucesso.setter
    def sucesso(self, value):
        self._sucesso = value

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario: UsuarioIn):
        self._usuario = usuario

    @property
    def sessao(self):
        return self._sessao

    @sessao.setter
    def sessao(self, operacoes: Session):
        self._sessao = operacoes

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request: Request):
        self._request = request

    @property
    def acao(self):
        return self._acao

    @acao.setter
    def acao(self, acao: str):
        self._acao = acao
