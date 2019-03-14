#! --*-- coding: utf-8 --*--
from logics.business import Business

def index(hm):
    mm = hm.mm
    business = Business(mm)
    rc, data = business.index()
    return rc, data

def handling(hm):
    mm = hm.mm
    auto = hm.get_argument('auto', is_int=True)
    select_id = hm.get_argument('select_id', is_int=True)
    if mm.business.business_times <= 0:
        return 3, {}  # 已处理完所有事务
    can_auto = mm.assistant.assistant
    if auto and not can_auto:
        return 1, {}  # 尚不能自动处理
    if not auto and not select_id:
        return 2, {}  # 请选择
    business = Business(mm)
    rc, data = business.handling(select_id, auto)
    return rc, data