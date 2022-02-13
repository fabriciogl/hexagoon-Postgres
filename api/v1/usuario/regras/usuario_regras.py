#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer
from api.v1.usuario.excecoes.usuario_excecoes import UsuarioCreateException, UsuarioUpdateException
from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario


class UsuarioRegras(RegrasInitiallizer):
    model: UsuarioIn
    data: Usuario

    def regra_1(self):
        """
        use : [create_1]
        """
        # Necessário passar por string para pegar casos deletados.
        resultado = self.handler.sessao \
            .execute("select * from usuario where email=:email",
                     {
                         'email': self.model.email
                     }
                     ) \
            .all()

        if resultado:
            raise UsuarioCreateException('Email informado possui cadastro. Utilize opção de recuperação de senha.')

    def regra_2(self):
        """
        use : [find_1, inactivate_1, update_1]

        verifica se o id existe e se está ativo
        """
        select_query = select(Usuario).where((Usuario.id == self._id) & (Usuario.ativo == True))
        try:
            self.data: Usuario = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'Usuário')

    def regra_3(self):
        """
        use : [update_2]

        verifica se trata-se de tentativa de alterar email do cadastro
        """

        if self.model.email:
            if self.data.email != self.model.email:
                raise UsuarioUpdateException('Não é possível alterar o email de cadastro.')

    def regra_4(self):
        """
        use : [softdelete_1]

        verifica se o id existe.
        """
        select_query = select(Usuario).where((Usuario.id == self._id))
        try:
            self.data: Usuario = self.handler.sessao.execute(select_query).scalar_one()
        except NoResultFound:
            raise SQLFindException(self._id, 'Usuário')
