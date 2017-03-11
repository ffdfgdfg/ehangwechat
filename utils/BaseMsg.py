# -*- coding: utf-8 -*-
class MsgBase:
    def MsgCheck(self, value):
        if len(value) is 0:
            return None
        else:
            return value
