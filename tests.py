# -*- coding: utf-8 -*-
from http_client import HttpClient
from sign import SignMixin


def test_sign():
    payload = {
        "exchange": "BITMEX"
    }
    print(SignMixin.join_dict(payload))
    assert SignMixin().sign(payload) == "9173fddc96e445b07a3d11295b52ca45385f96d9a52307da58134a2fd7e239be"


def test_contract():
    r = HttpClient(api_key="dWbkgDeLIzLavnYs", secret_key="dePW2XslyzFYnTuc41yRhqHIUWEVco4W", url="http://192.168.50.172/api/v1").contract_info("BITMEX")
    print(r.json())
    r = HttpClient(api_key="aYyjubTcVJveotCU", secret_key="aW2nGNZkJnfW6JaSvMZBG3DdFCmcVGyl").contract_info("BITMEX")
    print(r.json())


def test_account():
    r = HttpClient(api_key="aYyjubTcVJveotCU", secret_key="aW2nGNZkJnfW6JaSvMZBG3DdFCmcVGyl").account()
    print(r.json())
