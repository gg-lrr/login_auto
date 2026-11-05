import requests
from config.settings import BASE_URL

class HttpRequest:
    @staticmethod
    def send_post(path, data=None, json=None, headers=None):
        """封装post请求"""
        url = f"{BASE_URL}{path}"
        resp = requests.post(url=url, data=data, json=json, headers=headers)
        return resp