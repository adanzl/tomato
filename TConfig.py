#!/usr/bin/python
# -*- coding: UTF-8 -*-

class TConfig(object):

    def __init__(self, arg):
        super(TConfig, self).__init__()
        self.arg = arg

    pass

    T_TASK_WORK = 0
    T_TASK_REST = 1

    TASK_LIST = [
        {'type': T_TASK_WORK, 'msg': "正在煮番茄", 'music': ["music\\卡农.caf.mp3"], 'duration': 0.1 * 60},
        {
            'type': T_TASK_REST,
            'msg': "番茄煮好了",
            'music': [
                "music\\孙燕姿 - 同类.mp3"
                , "music\\孙燕姿 - 当冬夜渐暖.mp3"
                , "music\\孙燕姿 - 我怀念的.mp3"
                , "music\\孙燕姿 - 逆光.mp3"
            ],
            # 休息两首歌的时间
            'count': 2
        }
    ]

    ANIMATE_LiST = [
        {'pic': "img\\tomato.png"},
        # {'pic': "8.jpg"},
        # {'pic': "2.png"}
    ]

    ICO_WIDTH = 100
    ICO_HEIGHT = 100
