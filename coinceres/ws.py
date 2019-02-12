# -*- coding: utf-8 -*-
import json
import logging
import time

import websocket

logger = logging.getLogger(__name__)

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    print(message)
    print('------')
    print(ws.sock.recv_data())
    print('------')
    # pass


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(30):
            time.sleep(1)
            # ws.send("Hello %d" % i)
            ws.send(json.dumps({'msg_type': 'subscribe_tick', 'symbol': 'HUOBI/BTC_USDT'}))
            # payload = 'ping'
            # ws.send(payload)
        time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


def on_ping(*args, **kwargs):
    pass


class CeresSocketApp(websocket.WebSocketApp):

    def _send_ping(self, interval, event):
        while not event.wait(interval):
            self.last_ping_tm = time.time()
            if self.sock:
                try:
                    # payload = json.dumps({'msg_type': 'ping'}).encode("utf-8")
                    payload = 'ping'.encode('utf-8')
                    print('send ping')
                    self.sock.send(payload)
                except Exception as ex:
                    logger.warning("send_ping routine terminated: {}".format(ex))
                    break


class CeresWSClient(object):

    def __init__(self):
        self.url = ""
        self.api_key = ""
        self.event_ping = {}
        self.ws = None
        self.last_pong = 0
        self.session = None
        self.channels = list()

    def __del__(self):
        pass

    def keep_connection(self):
        pass

    def receive_data(self, payload: str):
        data = json.loads(payload)
        msg_type = data.get('msg_type')
        if msg_type == 'pong':
            self.last_pong = time.time()
            return

    def tick(self):
        pass

    def trade(self):
        pass

    def depth(self):
        pass

    def k_line(self):
        pass

    def restart(self):
        pass


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = CeresSocketApp("ws://192.168.50.172:18002/",
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close,)
    ws.on_open = on_open
    ws.run_forever(ping_interval=4)
    # ws.run_forever()
