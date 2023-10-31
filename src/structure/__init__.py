from copy import deepcopy
from typing import Any, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
    new = deepcopy(field)
    new.default = default
    new.annotation = Optional[field.annotation]  # type: ignore
    return (new.annotation, new)


BaseModelT = TypeVar('BaseModelT', bound=BaseModel)


def make_partial_model(model: Type[BaseModelT]) -> Type[BaseModelT]:
    return create_model(  # type: ignore
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
        )
