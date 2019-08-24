from models import Holder, BigItem, LittleItem, RogueItem
from pydantic import ValidationError


def test_list():

    h = Holder(items=list())

    h.items.append(LittleItem(c='a'))
    h.items.append(BigItem(a='a', b='b'))

    h_js = h.dict()
    print(h_js)


    try:
        h2 = Holder(**h_js)
    except ValidationError as e:
        print(e)
        assert False
    assert h == h2

def test_list2():

    h = Holder(items=list())

    h.items.append(LittleItem(c='a'))
    h.items.append(RogueItem(c=12.3, d='a'))

    h_js = h.dict()
    print(h_js)


    try:
        h2 = Holder(**h_js)
    except ValidationError as e:
        print(e)
        assert False
    assert h == h2