def get_lower_left(i):
    return 2 * i + 1

def get_lower_right(i):
    return 2 * i + 2

def heapify(data, i):
    left = get_lower_left(i)
    right = get_lower_right(i)
    size = len(data) - 1

    min = i
    if left <= size and data[min] > data[left]:
        min = left
    if right <= size and data[min] > data[right]:
        min = right
    if min != i:
        data[i], data[min] = data[min], data[i]
        heapify(data, min)

data = [6, 15, 4, 2, 8, 5, 11, 9, 7, 13]

#ヒープを構成
for i in reversed(range(len(data) // 2)):
    heapify(data, i)

#ソートを実行
sorted_data = []
for _ in range(len(data)):
    data[0], data[-1] = data[-1], data[0]#最後のノードと先頭を入れ替える
    sorted_data.append(data.pop())#最小のノードを取り出してソート済みにする
    heapify(data, 0)#ヒープを再構成

print(sorted_data)