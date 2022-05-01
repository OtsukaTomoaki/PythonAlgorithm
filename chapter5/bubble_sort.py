data = [6, 15, 4, 2, 8, 5, 11, 9, 7, 13]

change = True
for i in range(len(data)):
    if not change:
        break#バブルソートに変更が生じなかった場合は処理を打ち切る
    change = False
    print(data)
    for j in range(len(data) - i - 1):
        if data[j] > data[j + 1]:
            data[j], data[j + 1] = data[j + 1], data[j]
            change = True

print(data)