#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException

from api.v1.usuario.model.usuario_model import UsuarioIn


class AsUsuarioRoleRegrasException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(422, msg)


class AsUsuarioCreateException(HTTPException):
    """Exceção a ser utilizada quando ocorre erro na criacao de model"""

    def __init__(self, model: UsuarioIn, msg: str):
        """

        Args:
            model_name: string do nome do model
            i:  identificação do model
        """
        super().__init__(422, f'O {type(model).__name__} com email {model.email} não foi criado.')

