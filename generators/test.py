def source(limit):
    for i in range(0, limit):
        yield i


def prime_factors(num):
    i = 2
    while i * i <= num:
        if num % i:
            i += 1
        else:
            num //= i
            yield i
    if num > 1:
        yield num


def filter(num):
    if num % 2 == 1:
        yield num


for s in source(100):
    for f in prime_factors(s):
        for n in filter(f):
            print("{}:  {}".format(s, n))
