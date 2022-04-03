import pprint
maze = [
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
    [9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 9],
    [9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9],
    [9, 0, 9, 9, 0, 9, 0, 0, 0, 9, 0, 9],
    [9, 0, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9],
    [9, 9, 9, 0, 0, 9, 0, 9, 0, 0, 0, 9],
    [9, 0, 0, 0, 9, 0, 9, 0, 0, 9, 1, 9],
    [9, 0, 9, 0, 0, 0, 0, 9, 0, 0, 9, 9],
    [9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 0, 9],
    [9, 0, 9, 0, 9, 0, 9, 0, 0, 9, 0, 9],
    [9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9],
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
]

def search(x, y, depth):
    print(depth)
    pprint.pprint(maze)
    #ゴールに着くと終了
    if maze[x][y] == 1:
        print(depth)
        exit()
    
    #探索済みとしてセット
    maze[x][y] = 2

    next_depth = depth + 1
    #上下左右を探索
    if maze[x - 1][y] < 2:
        search(x - 1, y, next_depth)
    if maze[x + 1][y] < 2:
        search(x + 1, y, next_depth)
    if maze[x][y - 1] < 2:
        search(x, y -1, next_depth)
    if maze[x][y + 1] < 2:
        search(x, y + 1, next_depth)
    
    #探索前に戻す
    maze[x][y] = 0

#スタート位置から開始
search(1, 1, 0)