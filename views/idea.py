#! --*-- coding: utf-8 --*--


from models.idea import Idea


def add_msg(hm):
    mm=hm.mm
    msg = hm.get_argument('message','')
    if not msg:
        return 0, {}
    idea = Idea()
    idea.add_msg(mm.uid,msg)
    return 0, {}
