import sys
import pandas as pd
import numpy

#print時の行数が省略されてしまうので、最大の生徒数まで表示できる様にする
pd.set_option('display.max_rows', 200)
#落第点とする閾値の定義
SCORE_LOWER_LIMIT = 49
#printする落第点をとった教科の個数
DROP_SUBJECT_COUNT = 2

"""
指定個数の落第点をもつ生徒一覧のprint
"""
def getDropoutStudent(df, score_lower_limited, drop_subject_count):
    dropout_df = df.copy()
    #教科ごとに落第点以下の生徒一覧を取得する
    dropout_mathematics_df = dropout_df[dropout_df['Mathematics'] <= score_lower_limited][['ID']]
    dropout_science_df = dropout_df[dropout_df['Science'] <= score_lower_limited][['ID']]
    dropout_english_df = dropout_df[dropout_df['English'] <= score_lower_limited][['ID']]
    dropout_japanese_df = dropout_df[dropout_df['Japanese'] <= score_lower_limited][['ID']]
    dropout_history_df = dropout_df[dropout_df['History'] <= score_lower_limited][['ID']]
    dropout_geography_df = dropout_df[dropout_df['Geography'] <= score_lower_limited][['ID']]
    
    #落第点以下の生徒一覧を連結後、グループ化し、指定の個数以上の教科で落第した生徒を絞り込む
    dropout_concat_df = pd.concat(
        [
        dropout_mathematics_df, 
        dropout_science_df,
        dropout_english_df,
        dropout_japanese_df,
        dropout_history_df,
        dropout_geography_df])
    dropout_group_df = dropout_concat_df.groupby('ID').value_counts().reset_index(name='Count')
    dropout_group_df = dropout_group_df[(drop_subject_count <= dropout_group_df['Count'])]
    
    #ID順にソートして印刷
    dropout_group_df = dropout_group_df.sort_values(['ID'])
    return dropout_group_df[['ID']].to_csv(index=False)

"""
最高平均点、最低平均点もつ生徒一覧のprint
"""
def printTopVsBottom(df):
    mean_df = df.copy()

    #DataFrameにMean列を追加し、平均を格納する
    mean_df['Mean'] = df.mean(axis=1, numeric_only=True)

    #小数点第二位まで表示するように四捨五入する
    mean_df = mean_df.round({'Mean': 2})

    #最高平均点、最大平均点をそれぞれ取得し、該当の生徒を絞り込む
    max_avarage = mean_df['Mean'].max()
    min_avarage = mean_df['Mean'].min()
    found_df = mean_df[(mean_df['Mean'] == max_avarage) | (mean_df['Mean'] == min_avarage)]
    
    #Mean列、ID列でソートしてprintする
    #DataFrameをそのままprintした際、小数点以下が.00の場合に.0と表示されてしまう。
    #DataFrameのまま表示形式を変更することができなかったので、
    #ループして表示するデータを.00表示されるように加工しながらprintする
    found_df = found_df.sort_values(['Mean', 'ID'])
    found_df = found_df[['ID', 'Mean']]
    print(','.join(['ID', 'Mean']))

    for i, data in found_df[['ID', 'Mean']].iterrows():
        print(data['ID'] + ',' + '{:.2f}'.format(data['Mean']))

def main(argv):
    output_mode = argv[0]
    path_csv = argv[1]
    df = pd.read_csv(filepath_or_buffer=path_csv, encoding="utf8", sep=",")
    
    if 'dropouts' == output_mode:#落第点をもつ生徒一覧のprint
        print(getDropoutStudent(df, SCORE_LOWER_LIMIT, DROP_SUBJECT_COUNT))

    elif 'top-vs-bottom' == output_mode:#最高平均点、最低平均点をもつ生徒一覧の取得
        getTopVsBottom(df)

if __name__ == '__main__':
    main(sys.argv[1:])