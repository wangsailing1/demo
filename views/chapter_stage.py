# -*- coding: utf-8 –*-

from logics.chapter_stage import Chapter_stage
from models.vip_company import chapterstage_fastten, unlock_func_lv
from return_msg_config import i18n_msg


# 首页
def chapter_stage_index(hm):
    mm = hm.mm
    return 0, {'chapter': mm.chapter_stage.chapter,
               'next_chapter': mm.chapter_stage.next_chapter,
               'top_income': mm.script.top_all.get('finished_summary', {}).get('income', 0)}


# 打副本
def chapter_stage_fight(hm):
    mm = hm.mm
    stage = hm.get_argument('stage', '')
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    align = hm.get_argument('align', '')
    if not stage:
        return 1, {}  # 关卡参数错误
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight_new(stage, type_hard, align=align)
    return rc, data


# 剧情奖励
def get_dialogue_reward(hm):
    mm = hm.mm
    now_stage = hm.get_argument('now_stage', 0, is_int=True)
    choice_stage = hm.get_argument('choice_stage', 0, is_int=True)
    card_id = hm.get_argument('card_id', 0, is_int=True)
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.get_dialogue_reward(now_stage, choice_stage, card_id)
    return rc, data


# 解锁艺人聊天
def open_actor_chat(hm):
    mm = hm.mm
    now_stage = hm.get_argument('now_stage', 0, is_int=True)
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.open_actor_chat(now_stage)
    return rc, {'actor': data}


# 扫荡
def auto_sweep(hm):
    mm = hm.mm
    stage = hm.get_argument('stage', '')
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    if not mm.assistant.assistant and times == 1:
        return 'error_assistant', {}  # 请先聘请终身助理
    align = hm.get_argument('align', '')
    if times == 10 and not chapterstage_fastten(mm.user):
        lv = unlock_func_lv('chapterstage_fastten')
        return 2, {'custom_msg': i18n_msg.get(1210, mm.lan) % lv}  #
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight_new(stage, type_hard, auto=True, times=times, align=align)
    return rc, data

