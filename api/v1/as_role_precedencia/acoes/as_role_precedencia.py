#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from banco_dados.sql_alchemy.configuracao.data_schema import Role, AsRolePrecedencia


class AsRolePrecedenciaAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: AsRolePrecedencia
    data: AsRolePrecedencia

    def acao_0(self):
        """ use : [find_0, update_0, softdelete_0] """
        select_query = select(AsRolePrecedencia).filter_by(id=self._id)
        self.data: AsRolePrecedencia = self.handler.sessao.execute(select_query).scalar_one()

    def acao_1(self):
        """ use : [find_1] """
        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create_1] """
        # Seleciona o usuário
        select_sub_role = select(Role).filter_by(id=self.model.sub_role_id)
        sub_role: Role = self.handler.sessao.execute(select_sub_role).scalar_one()

        # Seleciona a role
        precedencia_role = select(Role).filter_by(id=self.model.precedencia_id)
        precedencia: Role = self.handler.sessao.execute(precedencia_role).scalar_one()

        #Cria o objeto Associacao
        self.data = AsRolePrecedencia(sub_role=sub_role, precedencia=precedencia)
        self.handler.sessao.add(self.data)


    def acao_3(self):
        """ use : [softdelete_1] """
        self.data.soft_delete()

    def acao_4(self):
        """ use : [update_1] """
        self.data.update(self.model)




