from typing import Generic, TypeVar, Any, List

from pydantic import BaseModel, create_model, Schema
from pydantic.generics import GenericModel


T = TypeVar('T')


class FileRef(BaseModel):
    name: str
    hash: str


def ModelStructure(name, TSpecializer=None, TCollection=None):
    contents = {
        "str_field": (str, Schema(..., description="A string field")),
        "dbl_field": (float, Schema(..., description="A float field")),
        "int_field": (int, Schema(..., description="An int field")),
        "obj_field": (BaseModel, Schema(..., description="An object field")),
    }

    class Config:
        arbitrary_types_allowed: True

    if TSpecializer is not None:
        for k, v in contents.items():
            inner_type, default = v
            if TCollection:
                contents[k] = TCollection[TSpecializer[inner_type]], default
            else:
                contents[k] = TSpecializer[inner_type], default


    model = create_model(name, **contents, __config__=Config)
    model.__doc__ = "Test model docstring description"

    return model

class TimeSeries(GenericModel, Generic[T]):
    """
    A time series value
    """

    ts: int = Schema(..., description="Timestamp of the data point")
    st: int = Schema(..., description="Salt of the data point")
    val: T = Schema(..., description="Value of the data point")


TimeModel = ModelStructure('TimeModel', TimeSeries)
TimeSeriesModel = ModelStructure('TimeSeriesModel', TimeSeries, List)
View = ModelStructure('View')


if __name__ == "__main__":

    print("=== view ===")
    v = View(
        str_field="test",
        dbl_field=1.23,
        int_field=321,
        obj_field={
            "name": "test.txt",
            "hash": "abc123"
        }
    )
    print(v.json())
    print(v.schema())


    print("=== Time ===")
    m = TimeModel(
        str_field={
            "ts": 1,
            "st": 1,
            "val": "Somestr"
        },
        dbl_field={
            "ts": 1,
            "st": 1,
            "val": 1.23
        },
        int_field={
            "ts": 1,
            "st": 1,
            "val": 321
        },
        obj_field={
            "ts": 1,
            "st": 1,
            "val": {
                "name": "test.txt",
                "hash": "abc123"
            }
        }
    )
    print(m.json())
    print(m.schema())


    print("=== time series ===")
    n = TimeSeriesModel(
        str_field=[{
            "ts": 1,
            "st": 1,
            "val": "Somestr"
        }],
        dbl_field=[{
            "ts": 1,
            "st": 1,
            "val": 1.23
        }],
        int_field=[{
            "ts": 1,
            "st": 1,
            "val": 321
        }],
        obj_field=[{
            "ts": 1,
            "st": 1,
            "val": {
                "name": "test.txt",
                "hash": "abc123"
            }
        }]
    )
    print(n.json())
    print(n.schema())