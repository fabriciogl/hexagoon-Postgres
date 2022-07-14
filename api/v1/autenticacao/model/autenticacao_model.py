#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from api.v1.role.model.role_model import RoleOut


class AutenticacaoIn(BaseModel):
    token: Optional[str]
    exp: Optional[datetime]

    class Config:
        title = 'tokens'
        orm_mode = True

class AutenticacaoOut(BaseModel):
    token: Optional[str]
    exp: Optional[datetime]
    roles: Optional[List[RoleOut]]

    class Config:
        orm_mode = True