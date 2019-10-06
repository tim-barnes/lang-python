from hashlib import sha1


def h(data):
    hfunc = sha1()
    hfunc.update(b"0")
    hfunc.update(str(data).encode('utf-8'))
    return hfunc.hexdigest()[:4]


def g(h1, h2):
    hfunc = sha1()
    hfunc.update(b"1")
    hfunc.update(h1.encode('utf-8'))
    hfunc.update(h2.encode('utf-8'))
    return hfunc.hexdigest()[:4]


def reduce(nodes):
    new_nodes = []
    i = 0
    try:
        while True:
            new_nodes.append(g(nodes[i], nodes[i+1]))
            i += 2
    except IndexError:
        # Off the end of the node list, if len is odd,
        # Append the hash of the last element
        if len(nodes) % 2:
            new_nodes.append(g(nodes[-1], '0'))

    return new_nodes


data = [1, 2, "foo", "bar", "coco", "toto", "bobo", 3.1415, 2.12]
data = data + data

nodes = [h(d) for d in data]

while len(nodes) > 1:
    print(nodes)
    nodes = reduce(nodes)

print(nodes)

