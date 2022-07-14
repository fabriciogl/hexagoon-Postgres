#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from config import settings
from api.v1.as_usuario_role.excecoes.as_usuario_role_exceptions import AsUsuarioRoleRegrasException
from api.v1.as_usuario_role.model.as_usuario_role_model import AsUsuarioRoleIn
from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario, Role, AsUsuarioRole


class AsUsuarioRoleRegras(RegrasInitiallizer):
    model: AsUsuarioRoleIn
    data: AsUsuarioRole

    def regra_1(self):
        """
        use : [create_1]
        """
        select_usuario = select(Usuario).filter_by(id=self.model.usuario_id)
        try:
            usuario = self.handler.sessao.execute(select_usuario).scalar_one()

        except NoResultFound:
            raise SQLFindException(self._id, 'usuário')

        select_role = select(Role).filter_by(id=self.model.role_id)
        try:
            role: Role = self.handler.sessao.execute(select_role).scalar_one()

        except NoResultFound:
            raise SQLFindException(self.model.role_id, 'role')

        if role.sigla in [a.role.sigla for a in usuario.a_roles]:
            raise AsUsuarioRoleRegrasException('Usuário possui a role informada.')

    def regra_2(self):
        """
        use : [find_1, inactivate_1, update_1, softdelete_1]

        verifica se o id existe e se está ativo
        """
        select_query = select(AsUsuarioRole).where(AsUsuarioRole.id == self._id)
        try:
            self.data = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'AsUsuarioRole')

    def regra_3(self):
        """
        use : [softdelete_2]

        verifica se o id é do usuário root e se irá deletar a role root (proíbe)
        """
        select_role = select(Role).where(Role.id == self.data.role_id)
        select_usuario = select(Usuario).where(Usuario.id == self.data.usuario_id)

        try:
            role: Role = self.handler.sessao.execute(select_role).scalar_one()
            usuario: Usuario = self.handler.sessao.execute(select_usuario).scalar_one()

            if role.sigla == settings.root_role \
                    and usuario.email == settings.root_email:
                raise AsUsuarioRoleRegrasException(msg='Não é possível remover a role do usuário root.')


        except NoResultFound:
            raise SQLFindException(self._id, 'AsUsuarioRole')
