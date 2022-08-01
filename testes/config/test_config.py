#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from config import settings


def test_config_env():
    assert settings.root_user
    assert settings.root_email
    assert settings.root_pass
    assert settings.jwt_algo
    assert settings.jwt_hash
