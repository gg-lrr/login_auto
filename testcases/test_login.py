import pytest
import requests

from config.settings import BASE_URL

class TestLogin:
    # 存放登录成功后的token，给后面鉴权用
    token = ""

    def test_login_success(self):
        """正向：账号密码正确，登录成功，拿到token"""
        url = f"{BASE_URL}/post"
        data = {
            "username": "test01",
            "password": "123456"
        }
        resp = requests.post(url, json=data)
        assert resp.status_code == 200
        res_json = resp.json()
        # 模拟返回token
        TestLogin.token = res_json["json"]["username"] + "_mock_token_123456"
        assert TestLogin.token is not None

    def test_login_wrong_password(self):
        """反向：账号正确、密码错误"""
        url = f"{BASE_URL}/post"
        data = {
            "username": "test01",
            "password": "654321"
        }
        resp = requests.post(url, json=data)
        assert resp.status_code == 200
        # 模拟业务码校验，识别密码错误
        assert resp.json()["json"]["password"] != "123456"

    def test_login_user_not_exist(self):
        """反向：账号不存在"""
        url = f"{BASE_URL}/post"
        data = {
            "username": "not_exist_user",
            "password": "123456"
        }
        resp = requests.post(url, json=data)
        assert resp.status_code == 200
        assert resp.json()["json"]["username"] == "not_exist_user"

    def test_login_username_empty(self):
        """反向：账号为空"""
        url = f"{BASE_URL}/post"
        data = {
            "username": "",
            "password": "123456"
        }
        resp = requests.post(url, json=data)
        assert resp.status_code == 200
        assert resp.json()["json"]["username"] == ""

    def test_login_pwd_empty(self):
        """反向：密码为空"""
        url = f"{BASE_URL}/post"
        data = {
            "username": "test01",
            "password": ""
        }
        resp = requests.post(url, json=data)
        assert resp.status_code == 200
        assert resp.json()["json"]["password"] == ""

    def test_token_auth(self):
        """后置场景：使用登录拿到的token访问需要鉴权的接口"""
        url = f"{BASE_URL}/headers"
        headers = {
            "Authorization": f"Bearer {TestLogin.token}"
        }
        resp = requests.get(url, headers=headers)
        assert resp.status_code == 200
        assert TestLogin.token in resp.json()["headers"]["Authorization"]