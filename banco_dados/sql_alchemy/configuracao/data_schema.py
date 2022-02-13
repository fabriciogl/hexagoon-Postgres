#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json
from datetime import datetime

from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, select, create_engine, event, JSON
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship, declared_attr, declarative_base, sessionmaker, Session, with_loader_criteria
from sqlalchemy_utils import database_exists, create_database
from starlette.requests import Request

from config import settings


# Funçao para converter o nome das classes para nome de tabelas
def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def snake_to_camel(s):
    return ''.join(word.title() for word in s.split('_'))


class BaseMixin:

    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    id = Column(Integer, primary_key=True, index=True)
    criado_em = Column(DateTime, default=func.now())
    alterado_em = Column(DateTime, onupdate=func.now())
    deletado_em = Column(DateTime)

    @declared_attr
    def alterador_id(cls):
        return Column(Integer, ForeignKey('usuario.id'))

    @declared_attr
    def alterado_por(cls):
        # Aqui ele quer o nome da classe e não da tabela
        return relationship("Usuario", foreign_keys=f"[{snake_to_camel(cls.__tablename__)}.alterador_id]")

    @declared_attr
    def criador_id(cls):
        return Column(Integer, ForeignKey('usuario.id'))

    @declared_attr
    def criado_por(cls):
        return relationship("Usuario", foreign_keys=f"[{snake_to_camel(cls.__tablename__)}.criador_id]")

    @declared_attr
    def deletador_id(cls):
        return Column(Integer, ForeignKey('usuario.id'))

    @declared_attr
    def deletado_por(cls):
        return relationship("Usuario", foreign_keys=f"[{snake_to_camel(cls.__tablename__)}.deletador_id]")

    def update(self, atributos: BaseModel):
        for atributo, valor in {**atributos.dict(exclude_none=True)}.items():
            self.__setattr__(atributo, valor)

    def soft_delete(self):
        self.__setattr__('deletado_em', datetime.now())

    @staticmethod
    def blame_insert(mapper, connection, target):
        if connection.connection.info.get('handler'):
            target.criador_id = connection.connection.info['handler'].usuario.id

    @staticmethod
    def blame_update(mapper, connection, target):
        if connection.connection.info.get('handler'):
            usuario = connection.connection.info['handler'].usuario

            if connection.connection.info['handler'].acao in ['update', 'inactivate']:
                target.alterador_id = usuario.id

            elif connection.connection.info['handler'].acao == 'softdelete':
                target.deletador_id = usuario.id
                target.deletado_em = datetime.now()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_insert', cls.blame_insert)
        event.listen(cls, 'before_update', cls.blame_update)


Base = declarative_base(cls=BaseMixin)


class AsUsuarioRole(Base):
    usuario_id = Column(ForeignKey('usuario.id'))
    role_id = Column(ForeignKey('role.id'))
    # exemplo de situação com relação many-to-one
    usuario = relationship("Usuario", back_populates="a_roles", foreign_keys=[usuario_id])
    # exemplo de situação com relação many-to-one
    role = relationship("Role", back_populates="a_usuarios", foreign_keys=[role_id])


class AsRolePrecedencia(Base):
    sub_role_id = Column(ForeignKey('role.id'))
    precedencia_id = Column(ForeignKey('role.id'))
    # exemplo de situação com relação many-to-one
    sub_role = relationship("Role", back_populates="a_precedencias", foreign_keys=[sub_role_id])
    # exemplo de situação com relação many-to-one
    precedencia = relationship("Role", back_populates="a_sub_roles", foreign_keys=[precedencia_id])


class Usuario(Base):
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    criador_id = Column(Integer, ForeignKey('usuario.id'))
    criado_por = relationship("Usuario", remote_side="[Usuario.id]", foreign_keys="[Usuario.criador_id]")
    alterador_id = Column(Integer, ForeignKey('usuario.id'))
    alterado_por = relationship("Usuario", remote_side="[Usuario.id]", foreign_keys="[Usuario.alterador_id]")
    deletador_id = Column(Integer, ForeignKey('usuario.id'))
    deletado_por = relationship("Usuario", remote_side="[Usuario.id]", foreign_keys="[Usuario.deletador_id]")

    # exemplo de situação com relação one-to-many
    a_roles = relationship(
        "AsUsuarioRole",
        # O default do cascade é 'save-update, merge', se for incluir algo, também incluir estes dois.
        back_populates='usuario',
        foreign_keys='[AsUsuarioRole.usuario_id]',
        cascade='save-update, merge'
    )


class Role(Base):
    descricao = Column(String(150))
    sigla = Column(String(10))

    # exemplo de situação com relação one-to-many
    a_usuarios = relationship(
        "AsUsuarioRole",
        # O default do cascade é 'save-update, merge', se for incluir algo, também incluir estes dois.
        back_populates='role'
    )

    # exemplo de situação com relação one-to-many
    a_precedencias = relationship(
        "AsRolePrecedencia",
        foreign_keys='[AsRolePrecedencia.sub_role_id]',
        back_populates='sub_role'
    )

    a_sub_roles = relationship(
        "AsRolePrecedencia",
        foreign_keys='[AsRolePrecedencia.precedencia_id]',
        back_populates='precedencia'
    )


class Artigo(Base):
    titulo = Column(String(150))
    corpo = Column(JSON)


class SQLSincrono:
    engine = None

    @staticmethod
    def create_engine() -> Engine:

        if not SQLSincrono.engine:
            engine = create_engine(
                f"{settings.db_driver}{settings.db_user}:{settings.db_pass}@{settings.db_address}",
                json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False)
            )
            # cria um banco de dados caso não exista
            if not database_exists(engine.url):
                create_database(engine.url)

            SQLSincrono.engine = engine

        return SQLSincrono.engine

    @staticmethod
    def create_session(request: Request = None) -> Session:
        Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=SQLSincrono.engine.connect()  # Por abrir uma conexão por sessão, também tem que fechar ao final.
        )

        # do_orm_execute captura todos os SELECT, mais os BULK update e delete
        # não captura update e delete individual
        # https://docs.sqlalchemy.org/en/14/orm/events.html (Execution Events)
        @event.listens_for(Session, "do_orm_execute")
        def _do_orm_execute(orm_execute_state):
            if (
                    orm_execute_state.is_select
                    and not orm_execute_state.is_column_load
                    and not orm_execute_state.is_relationship_load
            ):
                orm_execute_state.statement = orm_execute_state.statement.options(
                    with_loader_criteria(
                        BaseMixin,
                        lambda cls: cls.deletado_em.is_(None),  # SQLAlchemy não trabalha com is como igualdade.
                        include_aliases=True
                    )
                )

        session = Session()
        # o bloco try/finally funciona somente quando chamado dentro do Depends,
        # que deve ser chamado como parâmetro de uma função de requisicao.
        try:
            # A concessão do handler na forma seguinte é necessária quando não há
            # validação de role, nesse caso não há conhecimento de quem é o usuário da sessão
            # # pois ele é extraído do token jwt.
            # if request:
            #     handler = ResponseHandler(session=session)
            #     request.state._state['handler'] = handler
            yield session

        # o finally será executado somente após a resposta da requisicao
        finally:
            # Nos testes não há request
            if request and \
                    request.state._state.get('handler') \
                    and request.state._state['handler'].sucesso:

                session.commit()
                del request.state._state['handler']
            else:
                session.rollback()
            # fechar a sessão não fecha a conexão automaticamente,
            # tem que fazer as duas manualmente.
            session.bind.connection.close()
            session.close()

    @staticmethod
    def create_session_load_data() -> Session:
        session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=SQLSincrono.engine
        )()

        return session


def criar_tabelas():
    SQLSincrono.create_engine()
    Base.metadata.create_all(bind=SQLSincrono.engine)
    # Cria o usuário root
    session = SQLSincrono.create_session_load_data()
    if not session.execute(select(Role).filter_by(sigla="root")).fetchone():
        from banco_dados.sql_alchemy.load_data import load_data
        load_data(session)
