import environ
import os
import requests
import json
import time
import copy
from typing import Tuple

env = environ.Env()
base_dir = os.path.dirname(__file__)
env.read_env(os.path.join(base_dir,'.env'))

POPULATION_GOAL = 10000000

class PopulationCalculator:
    answer_list: list = []
    min_diff_total: int = 10000000

    def __init__(self) -> None:
        pass

class PopulationProvider():
    RESAS_API_ENDPOINT: str = 'https://opendata.resas-portal.go.jp'
    RESAS_API_KEY: str = env('RESAS_API_KEY')
    calculator: PopulationCalculator

    def __init__(self) -> None:
        self.prefectures = self.__fetch_prefectures()
        self.population = self.__fetch_population(self.prefectures)
        self.calculator = PopulationCalculator()
        print(self.population)

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
                'population': [x for x in population if x['year'] == 2015][0]['value'],
                'prefName': prefecture['prefName']
            }
            #サーバー負荷を下げるため0.3秒停止
            time.sleep(0.2)
        return  population_dict

    def find_population(self, min_diff_keys: list, goal: int):
        cur_answer: int = sum([v['population'] for k, v in self.population.items() if k in min_diff_keys])
        cur_diff: int = abs(cur_answer - goal)

        if cur_diff < self.calculator.min_diff_total:
            self.calculator.min_diff_total = cur_diff

        last_answer_index: int = min_diff_keys[-1]

        if self.calculator.min_diff_total == 0:
            pass  
        elif cur_answer < goal:
            next_answer_keys = copy.copy(min_diff_keys)
            self.find_population(next_answer_keys, goal) 

    # def calc(self, answer_keys: list, min_diff_answer: int, goal: int) -> Tuple[int, list]:
        
    #     last_answer_index: int = answer_keys[-1]
    #     cur_answer: int = sum([v['population'] for k, v in self.population.items() if k in answer_keys])
    #     exists_next_index: bool = (len(self.population) - 1) > last_answer_index

    #     next_answer = None
    #     #最後の要素を1つ増やす
    #     if exists_next_index:
    #         #リストを追加する(ゴール未満かつ現在まで計算した最小の差異よりも小さい場合に再起)
    #         if cur_answer < goal and abs(goal - min_diff_answer) > abs(goal - cur_answer):
    #             next_answer_keys = copy.copy(answer_keys)
    #             next_answer_keys.append(last_answer_index + 1)
    #             next_answer = self.calc(next_answer_keys, cur_answer, goal)
    #             #print(next_answer)
    #         #リストの末尾を１つ進める
    #         next_answer_keys = copy.copy(answer_keys[0:-1])
    #         next_answer_keys.append(last_answer_index + 1)
    #         _answer = self.calc(next_answer_keys, cur_answer, goal)
    #         if next_answer == None or (abs(goal - next_answer[0]) < abs(goal - next_answer[0])):
    #             next_answer = _answer

    #     if next_answer != None and abs(goal - next_answer[0]) < abs(goal - cur_answer):
    #         return next_answer
    #     else:
    #         return cur_answer, answer_keys



if __name__ == '__main__':
    prefectures = PopulationProvider()
    prefectures.loop()
