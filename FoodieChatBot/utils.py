import sys

def listToString(list):
    return ' '.join([str(x) for x in list])

def input():
    return sys.stdin.readline().strip()
