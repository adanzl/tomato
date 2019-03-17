#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json

SAVE_FILE = 'save.json'


class TUtil():
    @staticmethod
    def BuildTimeStr(str):
        return "%s" % (str)

    @staticmethod
    def BuildMsgStr(str):
        return "%s" % (str)

    @staticmethod
    def LoadSave(param=None):
        save = {}
        if not os.path.exists(SAVE_FILE):
            return save
        fo = open(SAVE_FILE, "r")
        saveStr = fo.read()
        print(saveStr)
        if saveStr.strip():
            save = json.loads(saveStr)
        fo.close()
        return save

    @staticmethod
    def SaveLocal(save):
        fo = open(SAVE_FILE, "w")
        saveStr = json.dumps(save)
        fo.write(saveStr)
        fo.close()
        return
