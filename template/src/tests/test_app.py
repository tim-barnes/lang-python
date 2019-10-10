import logging
from app import print_hello


def test_print_hello(caplog):
    caplog.set_level(logging.INFO)
    print_hello()
    for record in caplog.records:
        assert record.levelname == "INFO"
        assert record.message == "Hello World"
