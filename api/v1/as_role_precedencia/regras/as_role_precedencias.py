#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.as_role_precedencia.excecoes.as_role_precedencia import AsRolePrecedenciaException
from api.v1.as_role_precedencia.model.as_role_precedencia import AsRolePrecedenciaIn
from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario, Role, AsRolePrecedencia
from config import settings


class AsRolePrecedenciaRegras(RegrasInitiallizer):
    model: AsRolePrecedenciaIn
    data: AsRolePrecedencia

    def regra_1(self):
        """
        use : [create_1]
        """
        select_sub_role = select(Role).filter_by(id=self.model.sub_role_id)
        try:
            sub_role = self.handler.sessao.execute(select_sub_role).scalar_one()

        except NoResultFound:
            raise SQLFindException(self.model.sub_role_id, 'role')

        select_precedencia = select(Role).filter_by(id=self.model.precedencia_id)
        try:
            precedencia: Role = self.handler.sessao.execute(select_precedencia).scalar_one()

        except NoResultFound:
            raise SQLFindException(self.model.precedencia_id, 'role')

        if sub_role.sigla in [a.role.sigla for a in precedencia.a_sub_roles]:
            raise AsRolePrecedenciaException('Precedencia possui a role informada.')

    def regra_2(self):
        """
        use : [find_1, inactivate_1, update_1, softdelete_1]

        verifica se o id existe e se está ativo
        """
        select_query = select(AsRolePrecedencia).where(AsRolePrecedencia.id == self._id)
        try:
            self.data = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'AsRolePrecedencia')
