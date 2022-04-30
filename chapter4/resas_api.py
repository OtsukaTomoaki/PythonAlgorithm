import os
from dotenv import load_dotenv
import requests
import json
import time
import copy
from typing import Tuple

load_dotenv()

POPULATION_GOAL = 20000000

class PopulationCalculator:
    answer_list: list = []
    min_diff_total: int = POPULATION_GOAL

    def __init__(self) -> None:
        pass

class PopulationProvider():
    RESAS_API_ENDPOINT: str = 'https://opendata.resas-portal.go.jp'
    RESAS_API_KEY: str = os.environ['RESAS_API_KEY']
    calculator: PopulationCalculator

    def __init__(self) -> None:
        self.prefectures = self.__fetch_prefectures()
        self.population = self.__fetch_population(self.prefectures)
        self.calculator = PopulationCalculator()

    def __get_headers(self):
        return {
            'X-API-KEY' : self.RESAS_API_KEY
        }

    def __fetch_prefectures(self) -> json:
        url = self.RESAS_API_ENDPOINT + '/api/v1/prefectures'
        headers = self.__get_headers()

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        body_json = json.loads(response.text)
        prefectures = body_json['result']
        print(json.dumps(prefectures, indent=2))
        return prefectures

    def __fetch_population(self, prefectures: json) -> dict:
        headers = self.__get_headers()

        population_dict = {}
        for prefecture in prefectures:
            pref_code = prefecture['prefCode']

            url = self.RESAS_API_ENDPOINT + f'/api/v1/population/composition/perYear?cityCode=-&prefCode={pref_code}'

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            print(url, response.status_code)

            body_json = json.loads(response.text)
            result_data = body_json['result']['data']
            all_population = [x for x in result_data if x['label'] == '総人口']
            if len(all_population) < 1:
                return
            population = all_population[0]['data']

            #結果をdict形式で格納
            population_dict[pref_code] = {
                'population': [x for x in population if x['year'] == 2020][0]['value'],
                'prefName': prefecture['prefName']
            }
            #サーバー負荷を下げるため0.3秒停止
            time.sleep(0.2)
        return  population_dict

    def find_population(self, min_diff_keys: list, goal: int):
        cur_answer: int = sum([v['population'] for k, v in self.population.items() if k in min_diff_keys])
        cur_diff: int = abs(cur_answer - goal)
        print(min_diff_keys)
        #より正解に近い値が見つかった場合は正解を入れ替える
        if cur_diff < self.calculator.min_diff_total:
            self.calculator.min_diff_total = cur_diff
            self.calculator.answer_list = min_diff_keys

        last_answer_index: int = min_diff_keys[-1]

        if self.calculator.min_diff_total == 0:
            return min_diff_keys
        else:
            #正解よりも値が小さい場合はリストに要素を追加して再帰呼び出し
            if (cur_answer < goal) and (len(self.population) > last_answer_index):
                next_answer_keys = copy.copy(min_diff_keys)
                next_answer_keys.append(last_answer_index + 1)
                self.find_population(next_answer_keys, goal)
            #要素の最後の要素を1つ進めて再帰呼び出し
            if len(self.population) > last_answer_index:
                next_answer_keys = copy.copy(min_diff_keys[0: -1])
                next_answer_keys.append(last_answer_index + 1)
                self.find_population(next_answer_keys, goal)

if __name__ == '__main__':
    prefectures = PopulationProvider()
    prefectures.find_population([1], POPULATION_GOAL)
    print([v['prefName'] + ':' + str(v['population']) for k, v in prefectures.population.items() if k in prefectures.calculator.answer_list], prefectures.calculator.min_diff_total)
