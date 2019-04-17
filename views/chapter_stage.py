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
    if not mm.assistant.assistant:
        return 'error_assistant', {}  # 请先聘请终身助理
    stage = hm.get_argument('stage', '')
    times = hm.get_argument('times', 1, is_int=True)
    type_hard = hm.get_argument('type_hard', 0, is_int=True)
    align = hm.get_argument('align', '')
    if times == 10 and not chapterstage_fastten(mm.user):
        lv = unlock_func_lv('chapterstage_fastten')
        return 2, {'custom_msg': i18n_msg.get(1210, mm.lan) % lv}  #
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight_new(stage, type_hard, auto=True, times=times, align=align)
    return rc, data


# 故事会
def story_index(hm):
    mm = hm.mm
    if not mm.chapter_stage.story_unlock:
        return 1, {}  # 故事会尚未开启
    return 0, {
        'story_can_unlock': mm.chapter_stage.story_can_unlock,
        'story_unlock': mm.chapter_stage.story_unlock,
        'got_reward_story': mm.chapter_stage.got_reward_story
    }


# 讲故事
def story(hm):
    mm = hm.mm
    choice_id = hm.get_argument('choice_id', 0, is_int=True)
    now_stage = hm.get_argument('now_stage', 0, is_int=True)
    chapter_id = hm.get_argument('chapter_id', 0, is_int=True)
    if not mm.chapter_stage.story_unlock:
        return 1, {}  # 故事会尚未开启
    if not choice_id or not now_stage or not chapter_id:
        return 2, {}  # 章节数据出错了
    if chapter_id not in mm.chapter_stage.story_unlock:
        return 3, {}  # 故事未解锁
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.story(chapter_id, now_stage, choice_id)
    _, data_index = story_index(hm)
    data.updata(data_index)
    return rc, data


# 解锁
def unlock_story(hm):
    mm = hm.mm
    chapter_id = hm.get_argument('chapter_id', 0, is_int=True)
    if not mm.chapter_stage.story_unlock:
        return 1, {}  # 故事会尚未开启
    if chapter_id not in mm.chapter_stage.story_can_unlock:
        return 3, {}  # 请先听听前一个故事
    if chapter_id in mm.chapter_stage.story_unlock:
        return 4, {}  # 已经解锁过了
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.unlock_story(chapter_id)
    _, data_index = story_index(hm)
    data.updata(data_index)
    return rc, data
