# -*- coding: utf-8 -*-
"""
@Time ： 2022/3/31 13:58
@Auth ： Yan Zeyu
@File ： LeetCodeHelper.py
@IDE ： PyCharm

"""
import json

from datetime import datetime
from requests import Session, Response


class LeetCodeHelper:
    _login_url: str = 'https://leetcode-cn.com/accounts/login/'
    _leetcode_url: str = ''
    _login_header: dict = {
        'Referer': _login_url,
        "origin": 'https://leetcode-cn.com/'
    }
    _get_info_header: dict = {
        'content-type': 'application/json',
        'referer': 'https://leetcode-cn.com/problem-list/xb9nqhhg/',
        "origin": 'https://leetcode-cn.com/'
    }
    _query_payload: dict = {
        'problemsetQuestionsDynamicInfos': {
            "operationName": "problemsetQuestionsDynamicInfos",
            "variables": {},
            "query": "query problemsetQuestionsDynamicInfos {\n  problemsetQuestionsDynamicInfos {\n    questionId\n    frequency\n    solutionNum\n    isFavor\n    status\n    __typename\n  }\n}\n"
        }
    }

    _query_url: str = 'https://leetcode-cn.com/graphql/'

    def __init__(self, username: str, password: str):
        self.client: Session = Session()
        self.username: str = username
        self.password: str = password

    @property
    def _login_payload(self) -> dict:
        return {
            'login': self.username,
            'password': self.password
        }

    def _login(self) -> (bool, str):
        try:
            rep: Response = self.client.post(self._login_url, headers=self._login_header, data=self._login_payload,
                                             timeout=10)
            print(rep.status_code)
            # print(rep.text)
            return True, ''
        except Exception as e:
            return False, e

    def _query(self, operation: str) -> (bool, dict):
        try:
            rep: Response = self.client.post(self._query_url, headers=self._login_header,
                                             data=self._query_payload[operation])
            if rep.status_code == 200:
                return True, json.loads(rep.text)
            else:
                return False, {'data': f'query error, status_code: {rep.status_code}'}
        except Exception as e:
            return False, {'data': f'query error, exception: {e}'}

    def do(self, query: str) -> (bool, dict):
        today = datetime.now().strftime('%m/%d/%Y')

        success, message = self._login()
        if not success:
            print(f'{today} 登陆失败: {message}')
            return

        success, message = self._query(query)
        if not success:
            print(f'{today} 请求失败: {message}')
            return
        print(f'{today} 请求成功')

        if query == 'problemsetQuestionsDynamicInfos':
            for element in message['data']['problemsetQuestionsDynamicInfos']:
                del element['solutionNum']
                del element['isFavor']
                del element['acRate']
                del element['status']
                del element['__typename']

        with open(query, 'w') as file:
            print(message['data'])
            json.dump(message['data'], file)
        print(f'{today} 响应已保存')
        return True

