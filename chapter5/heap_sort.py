def get_lower_left(j):
    return 2 * j + 1

def get_lower_right(j):
    return 2 * j + 2

data = [6, 15, 4, 2, 8, 5, 11, 9, 7, 13]

#ヒープを構成
for i in range(len(data)):
    j = i
    while (j > 0) and (data[(j - 1) // 2] < data[j]):
        parent = (j - 1) // 2
        data[parent], data[j] = data[j], data[parent]#親と交換
        print(i, j, parent)
        j = parent
print(data)

#ソートを実行
for i in range(len(data), 0, -1):
    #ヒープの先頭と交換
    data[i - 1], data[0] = data[0], data[i - 1]
    j = 0
    #左下または右下が大きい場合
    while((get_lower_left(j) < i - 1) and (data[j] < data[get_lower_left(j)])) \
        or ((get_lower_right(j) < i - 1) and (data[j] < data[get_lower_right(j)])):

        if (get_lower_right(j) == i - 1) or (data[get_lower_left(j)] > data[get_lower_right(j)]):#左下の方が大きい時
            #左下と交換
            data[j], data[get_lower_left(j)] = data[get_lower_left(j)], data[j]
            #左下に移動
            j = get_lower_left(j)
        else:#右下の方が大きい時
            #右下と交換
            data[j], data[get_lower_right(j)] = data[get_lower_right(j)], data[j]
            #右下に移動
            j = get_lower_right(j)

print(data)