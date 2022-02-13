#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request

from banco_dados.sql_alchemy.configuracao.data_schema import Usuario


class TokenExpiredException(HTTPException):

    def __init__(self):
        """
        """
        super().__init__(401, f'O token jwt está expirado.')


class TokenException(HTTPException):

    def __init__(self, ordem: int, request: Request):
        msg = 'Token inválido.'
        match ordem:
            case 1:
                logging.warning(f'Header sem token {request.client.host}')
            case 2:
                logging.warning(f'Token expirado {request.client.host}')
                msg = 'Token expirado.'
            case 3:
                logging.warning(f'Token não integro {request.client.host}')
            case 4:
                logging.critical(f'Token com IP divergente {request.client.host}')

        super().__init__(401, msg)

class RoleException(HTTPException):

    def __init__(self, usuario: Usuario, request: Request):
        logging.critical(f'Usuário {usuario.email} tentou acessar {request.url} com método {request.method}')
        super().__init__(401, f'Usuário sem permissão.')

