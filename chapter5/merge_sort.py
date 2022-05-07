from turtle import right


data = [6, 15, 4, 2, 8, 5, 11, 9, 7, 13]

def merge_sort(data):
    print('data', data)
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    #再帰的に分割
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    #結合
    merge_data = merge(left, right)
    print('merge_data', merge_data)
    return merge_data

def merge(left, right):
    result = []
    i, j = 0, 0

    while (i < len(left)) and (j < len(right)):
        if left[i] <= right[j]: #左<=右の時
            result.append(left[i])
            i += 1
        else:#左>右の時
            result.append(right[j])
            j += 1

    #残りをまとめて追加
    if i < len(left):
        result.extend(left[i:])#結合
    if j < len(right):
        result.extend(right[j:])
    return result

print(merge_sort(data))


