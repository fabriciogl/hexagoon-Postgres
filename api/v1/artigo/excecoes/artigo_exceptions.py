#  Copyright (c) 2021. QuickTest app escrito por Fabricio Gatto Lourençone. Todos os direitos reservados.
from starlette.exceptions import HTTPException


class ArtigoRegrasException(HTTPException):

    def __init__(self, code: int, msg: str):
        super().__init__(code, msg)


class ArtigoCreateException(HTTPException):

    def __init__(self, msg: str):

        super().__init__(422, msg)



class ArtigoUpdateException(HTTPException):

    def __init__(self, msg: str):
        super().__init__(422, msg)
