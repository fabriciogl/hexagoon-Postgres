#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
from datetime import datetime

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def timeformat(input):
    return datetime.strftime(input, '%d/%m/%Y')

# adiciona filtros aos templates para serem utilizados por todas as chamadas
templates.env.filters["timeformat"] = timeformat


def create_templates():
    return templates
