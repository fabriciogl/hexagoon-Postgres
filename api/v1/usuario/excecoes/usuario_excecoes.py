#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request


class UsuarioRegrasException(HTTPException):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class UsuarioCreateException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(422, msg)

class UsuarioFindException(HTTPException):

    def __init__(self, ordem: int, _id: str, request: Request):
        msg = 'Token inválido'

        match ordem:
            case 1:
                logging.critical(f'Usuário do token inexistente {request.client.host}')

        super().__init__(401, msg)

class UsuarioUpdateException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(422, msg)
