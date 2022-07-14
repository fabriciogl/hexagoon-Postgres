#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from api.v1.role.model.role_model import RoleOut
from api.v1.usuario.model.usuario_model import UsuarioOutReduzido


class AsUsuarioRoleIn(BaseModel):
    usuario_id: Optional[int]
    role_id: Optional[int]


class AsUsuarioRoleOut(BaseModel):
    # Model de Usuário exclusivo da associacao
    # para evitar importacao cíclica
    class Usuario(BaseModel):
        id: int
        nome: str
        email: EmailStr

        class Config:
            orm_mode = True

    id: int
    usuario: UsuarioOutReduzido
    role: RoleOut
    criado_em: datetime

    class Config:
        orm_mode = True
