# -*- coding: utf-8 –*-

from logics.chapter_stage import Chapter_stage


# 首页
def chapter_stage_index(hm):
    mm = hm.mm
    return 0, {'chapter': mm.chapter_stage.chapter,
               'next_chapter': mm.chapter_stage.next_chapter}


# 打副本
def chapter_stage_fight(hm):
    mm = hm.mm
    stage = hm.get_argument('stage', '')
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    align = hm.get_argument('align', '')
    if not stage:
        return 1, {}  # 关卡参数错误
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight(stage, type_hard, align=align)
    return rc, data


# 剧情奖励
def get_dialogue_reward(hm):
    mm = hm.mm
    now_stage = int(hm.get_argument('now_stage', ''))
    choice_stage = int(hm.get_argument('choice_stage', ''))
    card_id = int(hm.get_argument('card_id', ''))
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.get_dialogue_reward(now_stage, choice_stage, card_id)
    return rc, data


# 解锁艺人聊天
def open_actor_chat(hm):
    mm = hm.mm
    now_stage = int(hm.get_argument('now_stage', ''))
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.open_actor_chat(now_stage)
    return rc, {'actor': data}


# 扫荡
def auto_sweep(hm):
    mm = hm.mm
    stage = hm.get_argument('stage', '')
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight(stage, type_hard, auto=True, times=times)
    return rc, data
