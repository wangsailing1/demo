#! --*-- coding: utf-8 --*--

__author__ = 'sm'


from admin import render
from admin.decorators import require_permission
from lib.core.environ import ModelManager
from gconfig import game_config


@require_permission
def select(req, **kwargs):
    """

    :param req:
    :return:
    """

    uid = req.get_argument('uid', '')
    result = {'private_city': None, 'uid': uid, 'msg': ''}
    result.update(kwargs)
    if uid:
        mm = ModelManager(uid)
        result['private_city'] = mm.private_city
        result['mm'] = mm

    return render(req, 'admin/private_city/index.html', **result)


@require_permission
def clearance(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    # mm.private_city.unlock_chapter = [i for i in game_config.chapter.iterkeys()]
    # mm.private_city.unlock_building = {}
    mm.private_city.final_chapter = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.use_building = {}
    mm.private_city.final_star = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.star = {}
    mm.private_city.finish = True

    mm.private_city.hard_final_chapter = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.hard_use_building = {}
    mm.private_city.hard_final_star = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.hard_star = {}
    mm.private_city.hard_finish = True

    mm.private_city.crazy_final_chapter = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.crazy_use_building = {}
    mm.private_city.crazy_final_star = [i for i in game_config.chapter.iterkeys()]
    mm.private_city.crazy_star = {}
    mm.private_city.crazy_finish = True

    mm.private_city.save()

    msg = 'success'

    return select(req, **{'msg': msg})


@require_permission
def update(req, **kwargs):
    """

    :param req:
    :param kwargs:
    :return:
    """
    uid = req.get_argument('uid', '')

    if not uid:
        return select(req, **{'msg': 'uid is not empty'})

    mm = ModelManager(uid)
    if mm.user.inited:
        return select(req, **{'msg': 'fail1'})

    chapter = int(req.get_argument('chapter', '1'))
    stage = int(req.get_argument('stage', '101'))
    degree = int(req.get_argument('degree', 1))

    stage_config = game_config.chapter.get(chapter, {}).get('stage', [])

    if stage not in stage_config:
        return select(req, **{'msg': 'chapter or stage error'})

    max_chapter = max(game_config.chapter)
    max_stage = max(game_config.chapter.get(max_chapter, {}).get('stage', []))
    degree_str = mm.private_city.degree_mapping[degree]

    finish = False
    final_chapter = [i for i in game_config.chapter.iterkeys() if i < chapter]
    final_star = final_chapter
    if stage_config[-1] == stage:
        use_building = {}
        star = {}
        final_chapter.append(chapter)
    else:
        use_building = {chapter: [game_config.chapter_to_stage[i][degree_str] for i in stage_config if i <= stage]}
        star = {chapter: {i: 3 for i in stage_config if i <= stage}}
    if max_chapter == chapter and max_stage == stage:
        finish = True

    if degree == 1:
        mm.private_city.final_chapter = final_chapter
        mm.private_city.use_building = use_building
        mm.private_city.final_star = final_star
        mm.private_city.star = star
        mm.private_city.finish = finish
    elif degree == 2:
        mm.private_city.hard_final_chapter = final_chapter
        mm.private_city.hard_use_building = use_building
        mm.private_city.hard_final_star = final_star
        mm.private_city.hard_star = star
        mm.private_city.hard_finish = finish
    else:
        mm.private_city.crazy_final_chapter = final_chapter
        mm.private_city.crazy_use_building = use_building
        mm.private_city.crazy_final_star = final_star
        mm.private_city.crazy_star = star
        mm.private_city.crazy_finish = finish

    mm.private_city.save()

    msg = 'success'

    return select(req, **{'msg': msg})
