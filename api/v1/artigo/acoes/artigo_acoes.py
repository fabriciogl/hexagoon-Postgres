#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.v1.artigo.model.artigo_model import ArtigoIn
from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.recursos.basic_exceptions.sql_exceptions import SQLFindException
from banco_dados.sql_alchemy.configuracao.data_schema import Artigo


class ArtigoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: ArtigoIn
    data: Artigo

    def acao_1(self):
        """ use : [find_1] """
        select_query = select(Artigo).filter_by(id=self._id)
        try:
            self.data = self.handler.sessao.execute(select_query).scalar_one()

        except NoResultFound:
            raise SQLFindException(self._id, 'Artigo')

        self.handler.sucesso = self.data

    def acao_2(self):
        """ use : [create_1] """
        self.data = Artigo(**self.model.dict())
        self.data.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.handler.sessao.add(self.data)


    def acao_3(self):
        """ use : [update_1] """
        select_query = select(Artigo).filter_by(id=self._id)
        try:
            self.data = self.handler.sessao.execute(select_query).scalar_one()

        except NoResultFound:
            raise SQLFindException(self._id, 'Artigo')

        # alterações
        self.model.titulo = self.model.corpo['blocks'][0]['data']['text']
        self.data.update(self.model)


    def acao_4(self):
        """ use : [softdelete_1] """
        select_query = select(Artigo).filter_by(id=self._id)

        try:
            if data := self.handler.sessao.execute(select_query).scalar_one():
                self.data = data

        except NoResultFound:
            raise SQLFindException(self._id, 'Role')

        self.data.soft_delete()

