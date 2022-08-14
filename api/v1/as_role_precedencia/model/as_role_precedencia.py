#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from api.v1.role.model.role_model import RoleOut
from api.v1.usuario.model.usuario_model import UsuarioOutReduzido


class AsRolePrecedenciaIn(BaseModel):
    sub_role_id: Optional[int]
    precedencia_id: Optional[int]


class AsRolePrecedenciaOut(BaseModel):
    id: int
    precedencia: RoleOut
    sub_role: RoleOut
    criado_em: datetime

    class Config:
        orm_mode = True
