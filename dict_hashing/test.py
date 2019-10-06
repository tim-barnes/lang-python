import hashlib

d1 = {
        'client': 'Unilever'
    }
d2 = {
        'client': 'Unilever',
        'brand': 'Magnum'
    }
d3 = {
        'client': 'Microsoft',
        'channel': 'chat'
    }
d4 = {
        'channel': 'chat',
        'client': 'Microsoft'
    }


def hash(d: dict):
    h = hashlib.sha1()

    for key in sorted(d.keys()):
        v = '{}={}'.format(key, d[key])
        h.update(v.encode('utf-8'))

    return h.hexdigest()[:4]


print("{}: {}".format(d1, hash(d1)))
print("{}: {}".format(d2, hash(d2)))
print("{}: {}".format(d3, hash(d3)))
print("{}: {}".format(d4, hash(d4)))
