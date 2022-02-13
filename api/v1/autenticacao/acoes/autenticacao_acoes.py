#  Copyright (c) 2022. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.

from datetime import datetime, timedelta

import jwt
from sqlalchemy import select

from api.v1.autenticacao.model.autenticacao_model import AutenticacaoOut
from api.v1.recursos.acoes_initiallizer import AcoesInitiallizer
from api.v1.usuario.model.usuario_model import UsuarioTokenIn
from banco_dados.sql_alchemy.configuracao.data_schema import Usuario
from config import settings
from templates.Jinja2 import create_templates

templates = create_templates()

class AutenticacaoAcoes(AcoesInitiallizer):
    # declara o tipo do model
    model: UsuarioTokenIn
    data: Usuario

    def acao_1(self):
        """ use : [login_1] """

        ip = self.handler.request.client.host
        expire = datetime.utcnow() + timedelta(hours=8)
        # atributo expire é reservado do jwt, atributo on eu criei para validacao do IP
        # mais informacoes na documentacao do PyJwt
        data = {"sub": self.handler.usuario.id, "on": ip, "exp": expire, 'roles': [a.role.sigla for a in self.handler.usuario.a_roles]}
        encoded_jwt = jwt.encode(
            payload=data,
            key=settings.hash_1,
            algorithm=settings.hash_2,
        )
        self.handler.sucesso = AutenticacaoOut(token=encoded_jwt, exp=expire, roles=[a.role for a in self.handler.usuario.a_roles])


    def acao_2(self):
        """ use : [recuperar_1] """

        select_query = select(Usuario).where(Usuario.email == self.model.email)
        usuario_data: Usuario = self.handler.sessao.execute(select_query).scalar_one()

        #TODO fazer um TASK Backgroud para enviar link por email
        usuario_data.ativo = True
        self.handler.sucesso = {'detail': 'Link enviado por email, verifique sua conta.'}
