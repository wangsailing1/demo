#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 用户相关的配置
from gconfig import check


# 内容弹幕
danmu = {
    'uk': ('stage_id', 'int'),  # 关卡id
    'dan_word': ('dan_word', 'list_2'),  # 弹幕内容

}


# 灌水弹幕
dan_word2 = {
    'uk': ('id', 'int'),
    'dan_word': ('dan_word', 'list_2'),  # 弹幕内容
}


# 冒险远征弹幕
danmu_pve = danmu
