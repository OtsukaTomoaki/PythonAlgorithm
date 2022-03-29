n = 18

#10進数を2進数に変換
def convert(n, base):
    result = ''
    while n > 0:
        result = str(n % base) + result
        n //= base
    return result

print(convert(n, 2))#2進数