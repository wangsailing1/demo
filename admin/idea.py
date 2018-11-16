#! --*-- coding: utf-8 --*--


from admin import render
from models.idea import Idea

def idea_index(req):
    idea = Idea()
    all_data = idea.get_msg()
    kwargs = dict(all_data=all_data)

    render(req, 'admin/idea/idea.html', **kwargs)

def del_msg(req):
    date = req.get_argument('date')
    key = req.get_argument('key')
    idea = Idea()
    idea.del_msg(date,key)
    all_data = idea.get_msg()
    kwargs = dict(all_data=all_data)

    render(req, 'admin/idea/idea.html', **kwargs)
