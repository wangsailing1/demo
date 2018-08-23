#! --*-- coding: utf-8 --*--

__author__ = 'sm'

from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config

MAX_NUM = 999

@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'item': None, 'gitem': None, 'citem': None, 'ggitem': None,
              'aitem': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['item'] = mm.item
        result['gitem'] = mm.grade_item
        result['citem'] = mm.coll_item
        result['ggitem'] = mm.guild_gift_item
        result['aitem'] = mm.awaken_item
        result['mm'] = mm

    return render(req, 'admin/item/index.html', **result)


@require_permission
def select_commander_part(req, **kwargs):
    """
    查询统帅碎片
    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'uid': uid, 'msg': '', 'commander_part': {}}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['commander_part'] = mm.commander.parts
        result['mm'] = mm

    return render(req, 'admin/item/commander_part_index.html', **result)


@require_permission
def commander_part_update(req, **kwargs):
    """
    统帅碎片更新
    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        part_id = int(req.get_argument('part_id'))
        part_num = int(req.get_argument('part_num'))

        mm.commander.parts[part_id] = part_num
    elif delete:
        part_id = int(req.get_argument('part_id'))

        mm.commander.parts.pop(part_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.commander.save()

    return select_commander_part(req, **{'msg': 'success'})


@require_permission
def select_commander(req, **kwargs):
    """
    查询统帅
    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')
    result = {'uid': uid, 'msg': '', 'commander_attrs': {}}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['commander_attrs'] = mm.commander.attrs
        result['mm'] = mm

    return render(req, 'admin/item/commander_index.html', **result)


@require_permission
def commander_update(req, **kwargs):
    """
    统帅更新
    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')

    if modify:
        commander_id = int(req.get_argument('commander_id'))
        commander_lv = int(req.get_argument('commander_lv'))
        commander_exp = int(req.get_argument('commander_exp'))

        mm.commander.attrs[commander_id] = {
            'exp': commander_exp,
            'lv': commander_lv,
        }
    else:
        return select(req, **{'msg': 'fail'})

    mm.commander.save()

    return select_commander(req, **{'msg': 'success'})


@require_permission
def item_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        item_id = int(req.get_argument('item_id'))
        item_num = int(req.get_argument('item_num'))

        mm.item.items[item_id] = item_num
    elif delete:
        item_id = int(req.get_argument('item_id'))

        mm.item.items.pop(item_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.item.save()

    return select(req, **{'msg': 'success'})


@require_permission
def gitem_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        gitem_id = int(req.get_argument('gitem_id'))
        gitem_num = int(req.get_argument('gitem_num'))

        mm.grade_item.items[gitem_id] = gitem_num
    elif delete:
        gitem_id = int(req.get_argument('gitem_id'))

        mm.grade_item.items.pop(gitem_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.grade_item.save()

    return select(req, **{'msg': 'success'})


@require_permission
def citem_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        citem_id = int(req.get_argument('citem_id'))
        citem_num = int(req.get_argument('citem_num'))

        mm.coll_item.items[citem_id] = citem_num
    elif delete:
        citem_id = int(req.get_argument('citem_id'))

        mm.coll_item.items.pop(citem_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.coll_item.save()

    return select(req, **{'msg': 'success'})


@require_permission
def ggitem_update(req, **kwargs):
    """

    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        ggitem_id = int(req.get_argument('ggitem_id'))
        ggitem_num = int(req.get_argument('ggitem_num'))

        mm.guild_gift_item.items[ggitem_id] = ggitem_num
    elif delete:
        ggitem_id = int(req.get_argument('ggitem_id'))

        mm.guild_gift_item.items.pop(ggitem_id, None)
    else:
        return select(req, **{'msg': 'fail'})

    mm.guild_gift_item.save()

    return select(req, **{'msg': 'success'})


@require_permission
def add_item(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_item.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_item.html', **result)

        params = req.get_reg_params(r'^item_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.item.add_item(param_name, param_value)

        mm.item.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_item.html', **result)


@require_permission
def add_gitem(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_gitem.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_gitem.html', **result)

        params = req.get_reg_params(r'^gitem_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.grade_item.add_item(param_name, param_value)

        mm.grade_item.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_gitem.html', **result)


@require_permission
def add_citem(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_citem.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_citem.html', **result)

        params = req.get_reg_params(r'^citem_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.coll_item.add_item(param_name, param_value)

        mm.coll_item.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_citem.html', **result)


@require_permission
def add_ggitem(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_ggitem.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_ggitem.html', **result)

        params = req.get_reg_params(r'^ggitem_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.guild_gift_item.add_item(param_name, param_value)

        mm.guild_gift_item.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_ggitem.html', **result)


@require_permission
def add_aitem(req, **kwargs):
    """
    送觉醒道具
    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_aitem.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_aitem.html', **result)

        params = req.get_reg_params(r'^aitem_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.awaken_item.add_item(param_name, param_value)

        mm.awaken_item.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_aitem.html', **result)


@require_permission
def add_commander_part(req, **kwargs):
    """
    送统帅碎片
    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_commander_part.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_commander_part.html', **result)

        params = req.get_reg_params(r'^part_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.commander.add_part(param_name, param_value)

        mm.commander.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_commander_part.html', **result)


@require_permission
def aitem_update(req, **kwargs):
    """
    更新觉醒道具
    :param req:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail'})

    modify = req.get_argument('modify', '')
    delete = req.get_argument('delete', '')

    if modify:
        aitem_id = int(req.get_argument('aitem_id'))
        aitem_num = int(req.get_argument('aitem_num'))

        diff_aitem = mm.awaken_item.items[aitem_id] - aitem_num
        if diff_aitem > 0:
            mm.awaken_item.del_item(aitem_id, diff_aitem)
        elif diff_aitem < 0:
            mm.awaken_item.add_item(aitem_id, -diff_aitem)
    elif delete:
        aitem_id = int(req.get_argument('aitem_id'))
        aitem_num = mm.awaken_item.items[aitem_id]
        mm.awaken_item.del_item(aitem_id, aitem_num)
    else:
        return select(req, **{'msg': 'fail'})

    mm.awaken_item.save()

    return select(req, **{'msg': 'success'})


@require_permission
def add_leader_skill(req, **kwargs):
    """
    送队长技能
    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    result = {'msg': '', 'uid': uid, 'max_num': MAX_NUM}

    if req.request.method == 'POST':
        if not uid:
            result['msg'] = 'uid is not empty'
            return render(req, 'admin/item/add_leader_skill.html', **result)
        mm = ModelManager(uid)

        if mm.user.inited:
            result['msg'] = 'fail'
            return render(req, 'admin/item/add_leader_skill.html', **result)

        params = req.get_reg_params(r'^skill_([0-9]+)$', value_filter=0)

        for param_name, param_value in params:
            if param_value > MAX_NUM:
                param_value = MAX_NUM
            mm.role_info.add_role_skill(param_name, param_value)

        mm.role_info.save()
        result['msg'] = 'success'

    return render(req, 'admin/item/add_leader_skill.html', **result)

