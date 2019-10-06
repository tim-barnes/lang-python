import etcd3
import logging
import os
import random
import time
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


try:
    etcd = etcd3.client(host=os.environ['ETCD_HOST'], port=os.environ['ETCD_PORT'])
except KeyError:
    _log.fatal("ETCD_HOST or ETCD_PORT not configured!")
    exit(1)


app = FastAPI()


@app.get("/")
def read_root():
    items =  etcd.get_all()
    items = { metadata.key: v for v, metadata in items }
    _log.debug(items)

    return items


@app.post("/{item}")
def post_item(item: str):
    i = f"{random.randint(0,100)}"
    etcd.put(f"/api/v1/{item}", i)
    return i


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
