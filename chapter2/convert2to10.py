from cgitb import reset
import re


n = '10010'

def convert(n, base):
    result = 0
    for i, val in enumerate(reversed(n)):
        result += int(val) * (base ** i)
    return result

print(convert(n, 2))


