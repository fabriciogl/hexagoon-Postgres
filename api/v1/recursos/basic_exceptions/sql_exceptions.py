#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from typing import Union

from starlette.exceptions import HTTPException


class SQLFindException(HTTPException):

    def __init__(self, i: Union[str, int], classe: str):
        super().__init__(406, f'Objeto {classe} sob id {i} não encontrado.')

class SQLException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(406, msg)

class SQLCreateException(HTTPException):

    def __init__(self):
        super().__init__(406, f'Não foi possível criar o objeto.')


class SQLUpdateException(HTTPException):

    def __init__(self, _id: Union[str, None] = None):
        super().__init__(422, f'Objeto sob id {_id} não foi alterado.')

class SQLDeleteException(HTTPException):

    def __init__(self, _id: str):
        super().__init__(422, f'Objeto sob id {_id} não encontrado.')
