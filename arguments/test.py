import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--env', nargs='*')

print(parser.parse_args(['--env', 'a=b', 'c=d', 'e=f']))

