#  Copyright (c) 2021. Hexagoon. Criador: Fabricio Gatto Lourençone. Todos os direitos reservados.
import re
from typing import Union, Type

from pydantic.types import ConstrainedStr, _registered

from api.v1.recursos.basic_exceptions.generic_validation_exceptions import GenericValidationException


class CustomIdValidation(ConstrainedStr):
    "Classe que sobreescreve Constrained para usar Exception específico"
    @classmethod
    def validate(cls, value: Union[str]) -> Union[str]:
        if cls.curtail_length and len(value) > cls.curtail_length:
            value = value[: cls.curtail_length]

        if cls.regex:
            if not cls.regex.match(value):
                raise GenericValidationException

        return value

def constr(
        *,
        strip_whitespace: bool = False,
        to_lower: bool = False,
        strict: bool = False,
        min_length: int = None,
        max_length: int = None,
        curtail_length: int = None,
        regex: str = None,
) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        strip_whitespace=strip_whitespace,
        to_lower=to_lower,
        strict=strict,
        min_length=min_length,
        max_length=max_length,
        curtail_length=curtail_length,
        regex=regex and re.compile(regex),
    )
    return _registered(type('ConstrainedStrValue', (CustomIdValidation,), namespace))

