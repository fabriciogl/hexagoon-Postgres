#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# class TestArtigoEndpoints: