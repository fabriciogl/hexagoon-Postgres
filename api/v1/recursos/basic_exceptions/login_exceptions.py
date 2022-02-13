#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
import logging

from starlette.exceptions import HTTPException
from starlette.requests import Request

from api.v1.usuario.model.usuario_model import UsuarioTokenIn


class LoginException(HTTPException):

    def __init__(self, ordem: int, usuario: UsuarioTokenIn, request: Request):
        msg = 'Usuário não identificado.'
        # match para identificar a mensagem de retorno
        match ordem:
            case 1:
                msg = f'Usuário com email {usuario.email} não encontrado.'
                logging.warning(f'Email inexistente {usuario.email}. IP {request.client.host}')
            case 2:
                msg = 'Usuário Inativo, para reativá-lo utilize recuperação de senha.'
                logging.warning(f'Tentativa de acesso com {usuario.email}. Usuário inativo. IP {request.client.host}')
            case 3:
                msg = 'Falha de autenticação.'
                logging.warning(f'Senha incorreta com {usuario.email}. IP {request.headers}')
            case _:
                msg = 'Usuário não identificado.'

        super().__init__(401, msg)
