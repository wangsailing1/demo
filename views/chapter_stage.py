# -*- coding: utf-8 –*-

from logics.chapter_stage import Chapter_stage

#首页
def chapter_stage_index(hm):
    mm = hm.mm
    return 0, {'chapter':mm.chapter_stage.chapter,
               'next_chapter':mm.chapter_stage.next_chapter}

#打副本
def chapter_stage_fight(hm):
    mm = hm.mm
    stage = hm.get_argument('stage', '')
    type_hard = int(hm.get_argument('type_hard',0))
    align = hm.get_argument('align','')
    print align
    if not stage:
        return 1, {} #关卡参数错误
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight(stage,type_hard,align=align)
    return rc,data

#扫荡
def auto_sweep(hm):
    mm = hm.mm
    stage = hm.get_argument('stage','')
    times = int(hm.get_argument('times',1))
    type_hard = int(hm.get_argument('type_hard', 0))
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage_fight(stage, type_hard,auto=True,times=times)
    return rc,data