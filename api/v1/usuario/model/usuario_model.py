#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from api.v1.role.model.role_model import RoleOutModel


class UsuarioIn(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]

    class Config:
        title = 'usuarios'

class UsuarioTokenIn(BaseModel):
    email: Optional[EmailStr]
    senha: Optional[str]


class UsuarioOut(BaseModel):
    class AsRole(BaseModel):
        role: RoleOutModel
        criado_em: datetime

        class Config:
            orm_mode = True

    id: int
    nome: str
    email: EmailStr
    a_roles: Optional[List[AsRole]]

    class Config:
        orm_mode = True

class UsuarioOutReduzido(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True