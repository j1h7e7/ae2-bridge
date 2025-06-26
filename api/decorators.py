from collections.abc import Callable
from typing import Any, Type, get_args

from flask_pydantic_api import pydantic_api as original_pydantic_api
from pydantic import BaseModel, RootModel, create_model


def pydantic_api(*args, **kwargs):  # TODO: type hints?
    """
    "Overloaded" so that I can properly handle non-pydantic types
    """

    def decorator(fn: Callable):
        annotations = fn.__annotations__

        for arg_name, type_hint in annotations.items():
            if new_type_hint := convert_to_pydantic(type_hint):
                annotations[arg_name] = new_type_hint

        return original_pydantic_api(*args, **kwargs)(fn)

    return decorator


def convert_to_pydantic(type_hint: Any) -> Type[BaseModel] | None:
    model_name, root_class = None, None

    if getattr(type_hint, "__origin__", None) is list:
        klass: type = get_args(type_hint)[0]
        model_name = f"List{klass.__name__}"
        root_class = list[klass]
    elif type_hint in [str, int, bool]:
        model_name = type_hint.__name__
        root_class = type_hint

    if model_name and root_class:
        return create_model(model_name, root=root_class, __base__=RootModel)

    return None
