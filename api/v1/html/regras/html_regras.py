#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLException
from api.v1.recursos.basic_exceptions.token_exceptions import RoleException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario, Artigo


class HTMLRegras(RegrasInitiallizer):

    model: UsuarioIn
    data: Usuario


    def regra_1(self):
        """
        use : [login_1]
        """
        pass

    def regra_2(self):
        """
        use : [admin_1]
        """
        can_access = False
        # roles originais
        roles_siglas = [a.role.sigla for a in self.handler.usuario.a_roles]
        # sub_roles
        roles = [a.role for a in self.handler.usuario.a_roles]
        a_sub_roles = [a_sub_roles for role in roles for a_sub_roles in role.a_sub_roles]
        all_sub_roles = [a.sub_role.sigla for a in a_sub_roles]
        # todas as roles
        all_roles = all_sub_roles + roles_siglas
        # verifica as roles necessárias para o endpoint
        for role in ['admin', 'root']:
            if role in all_roles:
                can_access = True

        if not can_access:
            raise RoleException(usuario=self.handler.usuario, request=self.handler.request)

    def regra_3(self):
        """
        use : [redirect_1]
        """
        pass

    def regra_4(self):
        """
        use : [article_1]
        """
        select_query = select(Artigo).where((Artigo.id == self._id))
        try:
            self.handler.sessao.execute(select_query).scalar_one()

        except NoResultFound:
            raise SQLException('O artigo solicitado não existe.')

    def regra_5(self):
        """
        use : [articleAll_1]
        """
        # # forma de se recuperar somente algumas colunas da tabela
        # select_query = select(Artigo.id, Artigo.titulo)
        #
        # try:
        #     self.handler.operacoes.execute(select_query).scalar_one()
        #
        # except NoResultFound:
        #     raise SQLException('Não há objetos do tipo artigo.')
