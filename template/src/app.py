import logging

_log = logging.getLogger()


def print_hello():
    _log.info("Hello World")
    print("Hello World")


if __name__ == "__main__":
    print_hello()
