import sys

def validateInputNum(num):
    if not num.isdecimal():
        print('整数を入力してください')
        sys.exit()

def validateChange(num):
    if num < 0:
        print('金額が不足しています')
        sys.exit()

if __name__ == '__main__':
    input_price = input('insert:')
    validateInputNum(input_price)

    product_price = input('product:')
    validateInputNum(product_price)

    change = int(input_price) - int(product_price)
    validateChange(change)
    
    coin = [5000, 1000, 500, 100, 50, 10, 5, 1]#紙幣、硬貨のリスト

    for i in coin:
        r = change // i
        change %= i
        print(str(i) + ': ' + str(r))
