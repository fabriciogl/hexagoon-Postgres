# Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os
# direitos reservados.
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.v1.as_role_precedencia.endpoint import as_role_precedencia_endpoints
from api.v1.as_usuario_role.endpoint import as_usuario_role_endpoints
from api.v1.autenticacao.endpoint import autenticacao_endpoints
from api.v1.recursos.basic_exceptions.generic_validation_exceptions import InvalidIdException
from api.v1.recursos.basic_exceptions.handler_exception import invalid_id
from api.v1.role.endpoint import role_endpoints
from api.v1.usuario.endpoint import usuario_endpoints
from banco_dados.sql_alchemy.configuracao.data_schema import criar_tabelas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=False,  # se vai aceitar cookies como credenciais
    allow_methods=["*"],  # métodos que o request pode apresentar para o backend
    allow_headers=["*"],  # atributos do headers que o request pode apresentar para o backend
    expose_headers=["Authorization"]  # atributos do headers que o browser pode acessar do response
)

app.mount("/estaticos", StaticFiles(directory="estaticos"), name="estaticos")

app.include_router(usuario_endpoints.router)
app.include_router(role_endpoints.router)
app.include_router(as_usuario_role_endpoints.router)
app.include_router(autenticacao_endpoints.router)
app.include_router(as_role_precedencia_endpoints.router)

app.add_event_handler("startup", criar_tabelas)
# app.add_event_handler("startup", iniciar_gcp_logger)

app.add_exception_handler(InvalidIdException, invalid_id)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Hexagoon (based on FastApi)",
        version="0.0.1",
        routes=app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/")
async def hello_world():
    return {"resultado": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
