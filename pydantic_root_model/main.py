from pydantic import BaseModel
from typing import Union, List

class Foo(BaseModel):
    qux: str


class Bar(BaseModel):
    baz: float


Members = Union[Foo, Bar]


class ChangedRoot(BaseModel):
    r: List[str]



if __name__ == "__main__":

    members_list = [
        Foo(qux="quux"),
        #Bar(baz=0.123),
        Foo(qux="coco")
    ]

    #model = ChangedRoot(__root__=members_list)
    model = ChangedRoot(r=['foo', 'bar', 'baz'])
    print(members_list)
    print(model)
    print(model.json(indent=2))


