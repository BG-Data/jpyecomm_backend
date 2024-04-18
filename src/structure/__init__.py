from copy import deepcopy
from typing import Any, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


class MakeOptionalPydantic:
    """Make all attributes from a Pydantic BaseModel Optional"""

    BaseModelT = TypeVar("BaseModelT", bound=BaseModel)

    @classmethod
    def make_field_optional(
        cls, field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return (new.annotation, new)

    @classmethod
    def make_partial_model(cls, model: Type[BaseModelT]) -> Type[BaseModelT]:
        return create_model(  # type: ignore
            f"Partial{model.__name__}",
            __base__=model,
            __module__=model.__module__,
            **{
                field_name: cls.make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()
            },
        )
