#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from api.v1.artigo.excecoes.artigo_exceptions import ArtigoCreateException
from api.v1.recursos.regras_initiallizer import RegrasInitiallizer


class ArtigoRegras(RegrasInitiallizer):

    def regra_1(self):
        """ use : [create_1, update_1] """
        data = self.model
        if data.corpo['blocks'][0]['type'] != 'header':
            raise ArtigoCreateException('O primeiro bloco do texto deve ser do tipo título.')

    def regra_2(self):
        """ use : [softdelete_1] """
        pass




