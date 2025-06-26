from datetime import datetime
from typing import Any

from flask.json.provider import DefaultJSONProvider
from pydantic import BaseModel


def jsonify(data: Any):
    match data:
        case str() | int():
            return data
        case list():
            return [jsonify(x) for x in data]
        case dict():
            return {k: jsonify(v) for k, v in data.items()}
        case BaseModel():
            return jsonify(data.model_dump())
        case datetime():
            return data.isoformat()
        case _:
            return data


class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        return super().dumps(jsonify(obj), **kwargs)
