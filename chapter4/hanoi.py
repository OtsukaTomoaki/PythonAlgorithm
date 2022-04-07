
def hanoi(n, src, dist, via):#高さ、移動元、移動先、経由場所
    if n > 1:
        hanoi(n - 1, src, via, dist)
        print(src + ' -> ' + dist, n)
        hanoi(n - 1, via, dist, src)
    else:
        print(src + ' -> ' + dist, n)
    
n = int(input())
hanoi(n, 'a', 'b', 'c')
