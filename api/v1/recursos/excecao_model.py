#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from pydantic.main import BaseModel


class Message(BaseModel):
    detail: str
