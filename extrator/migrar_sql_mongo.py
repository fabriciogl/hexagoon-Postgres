import json

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from banco_dados.sql_alchemy.configuracao.data_schema import Artigo

engine = create_engine(
    "postgresql://postgres:secret@0.0.0.0:5432/hexagoon",
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False)
)

sessao = Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)()

db = MongoClient('localhost', 27017).hexagoon

artigos = sessao.query(Artigo).all()

for artigo in artigos:
    db.artigos.insert_one({'corpo': artigo.corpo, 'titulo': artigo.titulo})


sessao.close()

