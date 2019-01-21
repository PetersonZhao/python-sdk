# -*- coding: utf-8 -*-
import requests

from sign import SignMixin


class HttpClient(SignMixin):
    """Http客户端"""
    def __init__(self, api_key, secret_key, url='http://open.coinceres.com/api/v1'):
        """
        :param api_key:
        :param secret_key:
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = url

    @staticmethod
    def join_url(*paths):
        return "/".join("{}".format(value) for value in paths)

    def _do_post(self, api: str, data: dict = None):
        headers = {'api_key': self.api_key, 'sign': self.sign(data)}
        r = requests.post(self.join_url(self.url, api), json=data, headers=headers)
        return r

    def _do_get(self, api: str, data: dict = None):
        headers = {'api_key': self.api_key, 'sign': self.sign(data)}
        r = requests.get(self.join_url(self.url, api), params=data, headers=headers)
        return r

    def _do_delete(self, api: str, data: dict = None):
        headers = {'api_key': self.api_key, 'sign': self.sign(data)}
        r = requests.delete(self.join_url(self.url, api), params=data, headers=headers)
        return r

    def contract_info(self, exchange: str, contract: str):
        """
        獲取交易所內各幣對基本信息
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :return:
        """
        data = {
            "exchange": exchange
        }
        if contract:
            data.update(contract=contract)
        return self._do_get(api="basic/contracts", data=data).json()

    def account(self, exchange: str = None):
        """
        獲取帳號信息
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :return:
        """
        data = None
        if exchange:
            data = {
                "exchange": exchange
            }
        return self._do_get(api="trade/account", data=data).json()

    def _order(self, exchange: str, contract: str, entrust_price: str, entrust_vol: str,
               entrust_bs: str, future_dir: str, lever: str, price_type: str):
        payload = {
            "contract": contract,
            "price_type": price_type,
            "entrust_bs": entrust_bs,
            "entrust_price": entrust_price,
            "entrust_vol": entrust_vol,
            "exchange": exchange,
            "future_dir": future_dir,
            "lever": lever,
        }
        return self._do_post("trade/input", data=payload).json()

    def market_order(self, exchange: str, contract: str, entrust_price: str, entrust_vol: str,
                     entrust_bs: str, future_dir: str, lever: str):
        """
        創建市價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_price: 委託價格
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :return:
        """
        return self._order(exchange, contract, entrust_price, entrust_vol, entrust_bs, future_dir, lever, "market")

    def limit_order(self, exchange: str, contract: str, entrust_price: str, entrust_vol: str,
                    entrust_bs: str, future_dir: str, lever: str):
        """
        創建限價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_price: 委託價格
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :return:
        """
        return self._order(exchange, contract, entrust_price, entrust_vol, entrust_bs, future_dir, lever, "limit")

    def delete_order(self, system_oid: str):
        """
        取消訂單
        :param system_oid: 訂單號
        :return:
        """
        payload = {
            "system_oid": system_oid
        }
        return self._do_delete("trade/order/", data=payload).json()

    def order_info(self, system_oid: str, status: int, exchange: str, contract: str):
        """
        查詢訂單詳情
        :param system_oid:                   系统生成订单号，逗号分隔，最多可查询15个
        :param status: 订单状态
        :param exchange: 交易所名稱
        :param contract: 幣對或合約名稱
        :return:
        """
        data = dict()
        if system_oid:
            data.update(system_oid=system_oid)
        if status:
            data.update(status=status)
        if exchange:
            data.update(exchange=exchange)
        if contract:
            data.update(contract=contract)
        if not data:
            data = None
        return self._do_get("trade/order", data=data).json()
