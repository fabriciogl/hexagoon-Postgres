#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from config import settings


def test_config_env():
    assert settings.root_user
    assert settings.root_email
    assert settings.root_senha
    assert settings.hash_1
    assert settings.hash_2
