from pydantic import BaseModel, validator, ValidationError
from typing import List, Union


class BigItem(BaseModel):
    a: str
    b: str


class LittleItem(BaseModel):
    c: str

class RogueItem(BaseModel):
    c: float
    d: str


class Holder(BaseModel):

    items: List[Union[BigItem, RogueItem, LittleItem]]

    # @validator('items', pre=True)
    # def convert_items(cls, v):
# 
    #     print(v)
    #     # raise ValueError()
    #     return v

