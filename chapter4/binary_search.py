def binary_search(data, value):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2 #小数点以下切り捨て
        if data[mid] == value:
            #中央の値と一致した場合は位置を返す
            return mid
        elif data[mid] < value:
            #valueの方が大きい場合は探索範囲の開始を変更
            left = mid + 1
        else:
            #valueの方が小さい場合は探索範囲の終了を変更
            right = mid - 1
    return -1

data = [10, 20, 30, 40, 50, 60, 70, 80, 90]
print(binary_search(data, 90))