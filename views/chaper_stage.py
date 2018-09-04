# -*- coding: utf-8 –*-


def chapter_stage(hm):
    mm = hm.mm
    user = mm.user

    return 0, {
        'dialogue_id':0,
        'stage_id':0,
        'star':0,
        'reward':{},
        'add_exp':0,
    }
    pass


def aotu_sweep(hm):
    mm = hm.mm
    user = mm.user
    stage = hm.get_argument('stage','')
    times = int(hm.get_argument('times',1))
    pass