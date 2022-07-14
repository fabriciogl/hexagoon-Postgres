#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

import inspect
import re
from abc import ABC
from operator import itemgetter
from typing import Callable, Union, re as t_re, Optional

from pydantic import BaseModel

from api.v1.recursos.response_handler import ResponseHandler


class RegrasInitiallizer(ABC):
    """ classe que contém o construtor das classes do tipo Regra"""
    def __init__(
            self,
            handler: ResponseHandler,
            regra: str,
            _id: Optional[Union[int, str]] = None,
            model: BaseModel = None
    ):
        self._id = _id
        self.model = model
        self.model_db = None
        self.handler = handler

        # verifica se a lista de acoes do objeto foi inicializada
        # metodo da classe instaciada
        self.create_list_rules()

        # Calable usa um conchetes com a primeira posição sendo os parametros, e a segunda o retorno
        method: Callable[[Union[str, BaseModel], ResponseHandler], None]

        # run the methods found in the action class
        # como estou chamando as actions em funcao da classe ligada ao primeiro objeto,
        # o self implicito dentro dos metodos sera sempre do primeiro objeto.
        for order, function in self.__class__.rules[regra]:
            if self.handler.sucesso:
                break
            else:
                function(self)

    @classmethod
    def create_list_rules(cls):
        """metodo que cria a lista de regras de cada classe instaciada de regras
           e salva em um dicionario criado na classe instaciada"""
        if not hasattr(cls, 'rules'):
            # cria um atributo na classe instaciada, chamado 'rules'
            setattr(cls, 'rules', {})
            # caso não tenha, aloca as regras e metodos de forma ordenada
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                doc_string = method.__doc__ if method.__doc__ else '' # evita erro de metodo/funcao sem docstring
                use_cases: t_re.Match = re.search(r'(?P<use>use\s{,4}[:=]{1,2}\s{,4}\[.*])', doc_string, flags=re.IGNORECASE)
                if use_cases and use_cases.group('use'):
                    # identifica todas as regras declaradas na funcao
                    list_uses = re.findall(r'\w*\d', use_cases.group('use'))
                    for use_order in list_uses:
                        use, order = use_order.split('_')
                        # Adicionei ao dicionario rules uma chave com o nome do metodo e valor
                        # após, uma chave com a ordem e o metodo como valor
                        cls.rules \
                            .setdefault(use, []) \
                            .append((int(order), method))

            # ordena a lista de metodos de cada regra
            for rule in cls.rules:
                cls.rules[rule].sort(key=itemgetter(0))