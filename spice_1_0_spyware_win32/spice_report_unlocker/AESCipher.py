#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import base64
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    BS = 16

    def __init__(self, key):
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

        if len(key) < 16:
            key = self.fill(key, 16 - len(key))

        elif (len(key) > 16) and (len(key) < 24):
            key = self.fill(key, 24 - len(key))

        elif (len(key) > 24) and (len(key) < 32):
            key = self.fill(key, 32 - len(key))

        elif len(key) > 32:
            key = key[0:32]

        self.key = key

    def Encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(raw))

    def Decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return self.unpad(cipher.decrypt(enc[16:]))

    def fill(self, key, extras):
        for i in range(extras):
            key += "0"

        return key