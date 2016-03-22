#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Zunayed Hassan'

import base64
from Crypto.Cipher import AES
from Crypto import Random

"""
CLASS NAME: AESCipher

PURPOSE:    Encrypting and decrypting text
"""
class AESCipher:
    BS = 16

    def __init__(self, key):
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

        # For AES encryption 16, 24 or 32 bit key required. But author's password might be more or less to our
        # required configuration. So, that's why we are checking password length and if something missing, then
        # we are tweaking password. But it won't effect to the original password that author gave.

        # If password length is less than 16, then make it 16 bit password by filling with zeroes (0) at the
        # end of the original password. The same thing is also done for 24 or  32  bit  or  more  length  of
        # passwords (if any).
        if len(key) < 16:
            key = self.fill(key, 16 - len(key))

        elif (len(key) > 16) and (len(key) < 24):
            key = self.fill(key, 24 - len(key))

        elif (len(key) > 24) and (len(key) < 32):
            key = self.fill(key, 32 - len(key))

        elif len(key) > 32:
            key = key[0:32]

        self.key = key


    """
    METHOD NAME:    Encrypt
    PARAMETER:      (string) raw
    RETURN:         string

    PURPOSE:        To encrypt string that author gave
    """
    def Encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(raw))


    """
    METHOD NAME:    Decrypt
    PARAMETER:      (string) enc
    RETURN:         string

    PURPOSE:        To decrypt text
    """
    def Decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return self.unpad(cipher.decrypt(enc[16:]))

    """
    METHOD NAME:    fill
    PARAMETER:      (string) key, (int) extras
    RETURN:         (string) key

    PURPOSE:        To fill up with zeroes (0) with string that give.

    EXAMPLE:        Input:  hello world, 5
                    Output: hello world00000
    """
    def fill(self, key, extras):
        for i in range(extras):
            key += "0"

        return key