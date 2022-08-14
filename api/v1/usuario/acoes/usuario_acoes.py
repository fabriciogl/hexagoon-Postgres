#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from passlib.hash import bcrypt
from sqlalchemy import select

from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario

class UsuarioAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioIn
    data: Usuario

    def acao_0(self):
        """ use: [find_1, update_1, inactivate_1] """
        select_query = select(Usuario).where((Usuario.id == self._id) & (Usuario.ativo == True))
        self.data: Usuario = self.handler.sessao.execute(select_query).scalar_one()


    def acao_1(self):
        """ use : [find_2] """
        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create_1] """
        # codifica a senha do usuario
        self.model.senha = bcrypt.using(rounds=7).hash(self.model.senha)
        # persiste o usuario
        self.data = Usuario(**self.model.dict(exclude_none=True))
        self.handler.sessao.add(self.data)

    def acao_3(self):
        """ use : [inactivate_2] """
        self.data.ativo = False
        self.handler.sucesso = {'resultado': 'usuário inativado.'}

    def acao_4(self):
        """ use : [update_2] """
        # Não é necessário adicionar na sessão, pois ao fazer a query o objeto já foi adicionado
        # e está em estado de observação. Os updates no objeto refletem diretamente no banco quando
        # do commit em função do unity of work implementado pelo SQLAlchemy
        self.data.update(self.model)

    def acao_5(self):
        """ use : [softdelete_1] """
        # Seleciona o usuário
        select_usuario = select(Usuario).where((Usuario.id == self._id))
        self.data = self.handler.sessao.execute(select_usuario).scalar_one()
        # Não é necessário adicionar na sessão, pois ao fazer a query o objeto já foi adicionado
        # e está em estado de observação.
        self.data.soft_delete()
