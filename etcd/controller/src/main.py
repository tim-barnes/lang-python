import etcd3
import logging
import os
import sys
import time

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


try:
    etcd = etcd3.client(
        host=os.environ['ETCD_HOST'], 
        port=os.environ['ETCD_PORT'],
        timeout=10
    )
except KeyError:
    _log.fatal("ETCD_HOST or ETCD_PORT not configured!")
    exit(1)


def increment(event):
    _log.debug(event)
    

if __name__ == "__main__":

    time.sleep(2)
    print(f"Testing connection {etcd.get('/api/v1/testkey')}")
    

    print("Started controller")
    events, cancel = etcd.watch("/api/v1/testkey")
    count = 0
    for event in events:
        print(event)
        count += 1
        if count > 10:
            cancel()

        etcd.put("/api/v1/testkey/controller", f"{event} eaten")

        sys.stdout.flush()
        

    #etcd.cancel_watch(watch_id)
    