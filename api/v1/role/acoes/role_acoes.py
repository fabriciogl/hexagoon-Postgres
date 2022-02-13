#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.role.model.role_model import RoleInModel
from banco_dados.sql_alchemy.configuracao.data_schema import Role as RoleData


class RoleAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: RoleInModel
    data: RoleData

    def acao_0(self):
        """ use : [find_1, inactivate_1, update_1, softdelete_1] """
        select_query = select(RoleData).filter_by(id=self._id)
        self.data: RoleData = self.handler.sessao.execute(select_query).scalar_one()

    def acao_1(self):
        """ use : [find_2] """
        self.handler.sucesso = self.data


    def acao_2(self):
        """ use : [create_1] """
        # cria o id do usuario
        self.data = RoleData(**self.model.dict())
        self.handler.sessao.add(self.data)
        # O refresh resolve o caso de objetos sofrendo lazy load após uma sessão ser encerrada.
        # outra solução é usar o parametro expire_on_commit para falso
        # self.handler.operacoes.refresh(self.data)

        self.handler.sessao.flush()
        self.handler.sucesso = self.data

    def acao_3(self):
        """ use : [update_2] """
        self.data.update(self.model)


    def acao_4(self):
        """ use : [softdelete_2] """
        self.data.soft_delete()

