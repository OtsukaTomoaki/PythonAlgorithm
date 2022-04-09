import os

def search(dir, name):
    for i in os.listdir(dir):
        current = dir + '/' + i
        if i == name:
            print(current)
        if os.path.isdir(current):
            if os.access(current, os.R_OK):
                search(current + '/', name)
search('/Users/ootsuka-tomoaki/Desktop', 'queen.py')