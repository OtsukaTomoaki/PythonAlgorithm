import functools

M, N = 6, 5

@functools.lru_cache(maxsize=None)#再起処理のメモ化
def search(m, n):
    if (m == 0) or (n == 0):
        return 1
    return search(m - 1, n) + search(m, n - 1)

print(search(M, N))