# -*- coding: utf-8 -*-
from http_client import HttpClient
from sign import SignMixin


def test_sign():
    payload = {
        "exchange": "BITMEX"
    }
    assert SignMixin().sign(payload) == "9173fddc96e445b07a3d11295b52ca45385f96d9a52307da58134a2fd7e239be"


def test_contract():
    r = HttpClient(api_key="dWbkgDeLIzLavnYs", secret_key="dePW2XslyzFYnTuc41yRhqHIUWEVco4W", host="192.168.50.172").contract_info("BITMEX")
    print(r)
    r = HttpClient(api_key="aYyjubTcVJveotCU", secret_key="aW2nGNZkJnfW6JaSvMZBG3DdFCmcVGyl").contract_info("BITMEX")
    print(r)


def test_account():
    r = HttpClient(api_key="aYyjubTcVJveotCU", secret_key="aW2nGNZkJnfW6JaSvMZBG3DdFCmcVGyl").account()
    print(r)


def test_order():
    r = HttpClient(api_key="dWbkgDeLIzLavnYs", secret_key="dePW2XslyzFYnTuc41yRhqHIUWEVco4W",
                   host="192.168.50.172").limit_order("BITMEX", "ADA_BTC", "10", "buy", "open", "10", "0.000011", "0.00000997")
    print(r)
