#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import json

from starlette.requests import Request
from starlette.responses import JSONResponse

from api.v1.recursos.basic_exceptions.generic_validation_exceptions import InvalidIdException


# from API.V1.Excecoes.BasicExceptions.MongoExceptions import MongoFindException2


def invalid_id(request: Request, exc: InvalidIdException):
    try:
        print(
            f'IP {request.client.host} - Port {request.client.port} - {request.headers.values()} - {request.path_params}')
    except json.decoder.JSONDecodeError as e:
        # Request had invalid or no body
        print(e)

    return JSONResponse({"detail": exc.detail}, status_code=404)
