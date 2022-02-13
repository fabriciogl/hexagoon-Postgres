#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from banco_dados.sql_alchemy.configuracao.data_schema import Role


class RoleRegras(RegrasInitiallizer):

    def regra_1(self):
        """
        use : [find_1, inactivate_1, update_1, softdelete_1]

        verifica se o id existe e se está ativo
        """
        select_query = select(Role).where(Role.id == self._id)
        try:
            self.data: Role = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'Role')