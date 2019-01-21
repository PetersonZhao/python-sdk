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
        return requests.post(self.join_url(self.url, api), json=data, headers=headers)

    def _do_get(self, api: str, data: dict = None):
        headers = {'api_key': self.api_key, 'sign': self.sign(data)}
        if data is None:
            return requests.get(self.join_url(self.url, api), headers=headers)
        return requests.get(self.join_url(self.url, api), params=data, headers=headers)

    def _do_delete(self, api: str, data: dict = None):
        headers = {'api_key': self.api_key, 'sign': self.sign(data)}
        return requests.delete(self.join_url(self.url, api), params=data, headers=headers)

    def contract_info(self, exchange: str, contract: str = None):
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

    def order_info(self, system_oid: str = None, status: int = None, exchange: str = None, contract: str = None):
        """
        查詢訂單詳情
        :param system_oid: 系统生成订单号，逗号分隔，最多可查询15个
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

    def _order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
               lever: str, price_type: str, entrust_price: str = None, profit_value: str = None,
               stop_value: str = None, client_oid: str = None):
        payload = {
            "exchange": exchange,
            "contract": contract,
            "price_type": price_type,
            "entrust_vol": entrust_vol,
            "entrust_bs": entrust_bs,
            "future_dir": future_dir,
            "lever": lever,
        }
        if entrust_price:
            payload.update(entrust_price=entrust_price)
        if profit_value:
            payload.update(profit_value=profit_value)
        if stop_value:
            payload.update(stop_value=stop_value)
        if client_oid:
            payload.update(client_oid=client_oid)
        return self._do_post("trade/input", data=payload).json()

    def market_order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
                     lever: str, entrust_price: str = None, profit_value: str = None, stop_value: str = None,
                     client_oid: str = None):
        """
        創建市價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_price: 委託價格
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :param profit_value: 止盈价,合约必传
        :param stop_value: 止损价，合约必传
        :param client_oid: 来源标记
        :return:
        """
        return self._order(exchange, contract, entrust_vol, entrust_bs, future_dir, lever, "market",
                           entrust_price, profit_value, stop_value, client_oid)

    def limit_order(self, exchange: str, contract: str, entrust_vol: str, entrust_bs: str, future_dir: str,
                    lever: str, entrust_price: str = None, profit_value: str = None, stop_value: str = None,
                    client_oid: str = None):
        """
        創建限價訂單
        :param exchange: 交易所名稱 OKEX,BINANCE,HUOBI,BITFINEX,BITMEX
        :param contract: 幣對或合約名稱
        :param entrust_price: 委託價格
        :param entrust_vol: 交易量
        :param entrust_bs: 交易方向 "buy"/"sell"
        :param future_dir: "open"/"close"
        :param lever: 槓桿倍數
        :param profit_value: 止盈价,合约必传
        :param stop_value: 止损价，合约必传
        :param client_oid: 来源标记
        :return:
        """
        return self._order(exchange, contract, entrust_vol, entrust_bs, future_dir, lever, "limit",
                           entrust_price, profit_value, stop_value, client_oid)

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

    def open_contract(self, exchange: str = None, contract: str = None, position_dir: str = None):
        """
        查询合约持仓信息
        :param exchange: 交易所名称
        :param contract: 合约名称
        :param position_dir: 持仓方向，多: "buy"/空: "sell"
        :return:
        """
        data = dict()
        if exchange:
            data.update(exchange=exchange)
        if contract:
            data.update(contract=contract)
        if position_dir:
            data.update(position_dir=position_dir)
        if not data:
            data = None
        return self._do_get("trade/position", data=data).json()

    def transaction(self, exchange: str, contract: str, count: int):
        """
        查询成交纪录
        :param exchange: 交易所名称
        :param contract: 币币交易对或合约名称
        :param count: 查询数量 最大50
        :return:
        """
        data = dict(
            exchange=exchange,
            contract=contract,
            count=count
        )
        return self._do_get("trade/trans", data=data).json()
