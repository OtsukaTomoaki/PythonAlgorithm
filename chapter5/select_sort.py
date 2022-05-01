data = [6, 15, 4, 2, 8, 5, 11, 9, 7, 13]

for i in range(len(data)):
    data_min = i
    for j in range(i + 1, len(data)):
        if data[data_min] > data[j]:
            data_min = j
    #最小値の位置と現在の要素の位置を交換
    data[i], data[data_min] = data[data_min], data[i]

print(data)