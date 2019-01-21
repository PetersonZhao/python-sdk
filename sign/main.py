# -*- coding: utf-8 -*-
import hashlib
import copy


class SignMixin(object):
    secret_key = "TQAFrtRS4WrUn1hHKByszao3ozWvIMkF"

    @classmethod
    def join_dict(cls, payload: dict):
        return "&".join("{}={}".format(key, value) for key, value in payload.items())

    def sign(self, data: dict = None):
        payload = copy.deepcopy(data)
        if payload is None:
            payload = dict()
        payload.update({"secret": self.secret_key})
        pre_sign = self.join_dict(payload)
        return hashlib.sha256(pre_sign.encode("utf8")).hexdigest()
