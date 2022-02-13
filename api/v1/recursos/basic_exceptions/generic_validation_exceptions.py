#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException


class InvalidIdException(HTTPException):
    """Exceção a ser utilizada quando a string de busca não é válida"""
    def __init__(self, http_code: int, message: str):
        super().__init__(http_code, message)


class GenericValidationException(InvalidIdException):
    """Exceção de string de identificacao inválida"""

    def __init__(self):
        super().__init__(404, f'Objeto não localizado.')