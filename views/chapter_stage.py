# -*- coding: utf-8 –*-

from logics.chapter_stage import Chapter_stage

def chapter_stage(hm):
    mm = hm.mm
    user = mm.user
    stage = hm.get_argument('stage', '')
    type_hard = hm.get_argument('type_hard','')
    align = hm.get_argument('align','')
    if not stage:
        return 1, {} #关卡参数错误
    chapter_stage = Chapter_stage(mm)
    rc, data = chapter_stage.chapter_stage(stage,type_hard,align)
    return rc,data


def aotu_sweep(hm):
    mm = hm.mm
    user = mm.user
    stage = hm.get_argument('stage','')
    times = int(hm.get_argument('times',1))
    pass