#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 采集相关的配置
from gconfig import check


# 采集英雄体力与能力计算
collection_weary = ({
    'uk': ('weary', 'int'),  # 体力
    'percent': ('percent', 'int'),  # 采集能力100%
}, 'collection_weary')


# 资源兑换
resource_exchange = {
    'uk': ('quality', 'int'),  # 品阶
    'give_num': ('give_num', 'int'),  # 产出数量
}


# 采集活动通知对话
activity_dialogue = {
    'uk': ('id', 'int'),  # id
    'sort': ('sort', 'int'),  # 场景
    'type': ('type', 'int'),  # 类型
    'dialogue': ('dialogue', 'unicode'),  # 对话内容
    'start_time': ('start_time', 'str'),  # 起始时间
    'end_time': ('end_time', 'str'),  # 结束时间
}
