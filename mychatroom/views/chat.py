#！ --*-- encoding:utf8 --*--
import time
from logics.chat import Chat
from models.user import UserData
from logics import ModelManager

def search_account(hm):
    mm = hm.mm
    account = hm.get_argument('account', '')
    user = UserData.get(account)
    if user.inited or not account:
        return 1, {'msg':'账号信息有误'}
    return 0,{'msg':'搜索成功','name':user.name, 'account':user.account}

def send_friend_application(hm):
    mm = hm.mm
    acc = hm.req.get_current_user()
    chat = Chat(mm)
    chat = public(chat, mm)
    rc, data = chat.add_friend_msg(acc)
    if rc != 0:
        return rc, data
    chat.content.save()
    return 0,{'msg':'已经向好友发起申请','name':mm.user.name}

def get_application(hm):
    mm = hm.mm
    chat = Chat(mm)
    if chat.content.inited or not chat.content.messages:
        return 1, {'msg':"当前没有申请信息"}
    return 0,{'msg':"ok", 'data':chat.content.messages}

def agree_add_friend(hm):
    mm = hm.mm
    acc = hm.get_argument('account', '')
    is_agree = hm.get_argument('is_agree', '', is_int=True)
    chat = Chat(mm)
    chat = public(chat, mm)
    chat.content.add_friend(acc)
    m1 = ModelManager(acc)
    chat = Chat(m1)
    chat = public(chat, m1)
    chat.content.agree_add(mm.user.account, is_agree)
    chat.content.save()
    return 0, {}

def get_friends(hm):
    mm = hm.mm
    chat = Chat(mm)
    chat = public(chat, mm)
    if not chat.content.friends:
        return 1, {'msg':'当前没有好友信息'}
    return 0,{'msg':'ok','data':chat.content.friends,'account':mm.user.account}

def action_chat(hm):
    mm = hm.mm
    friend = hm.get_argument('friend', '')
    chat = Chat(mm)
    chat = public(chat, mm)
    friend = chat.content.friends.get(friend, {})
    friend['new_msg'] = []
    if not friend:
        return 1, {"msg":'没有该好友'}
    chat.content.save()
    return 0, {'msg':'ok', 'data':{'msg':friend['msg'], 'new_msg':len(friend['new_msg'])}, 'name':friend['name'], 'account':friend['account']}

def send_msg(hm):
    mm = hm.mm
    account = hm.get_argument('friend', '')
    data = hm.get_argument('data', '')
    data1 = (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'me', data)
    chat = Chat(mm)
    chat = public(chat, mm)
    chat.send_message(account, data1)
    m1 = ModelManager(account)
    chat = Chat(m1)
    chat = public(chat, m1)
    # Chat.USER_QUEUE_DICT[mm.user.account].put(mm.user.account)
    # if Chat.USER_QUEUE_DICT.get(account):
    #     Chat.USER_QUEUE_DICT[account].put(mm.user.account)
    data = (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'you', data)
    chat.content.accept_msg(mm.user.account, data)
    chat.content.save()
    mm.do_save()
    return 0, {'mes':'ok'}

def public(chat, mm):
    if chat.content.inited:
        chat.content.save()
        chat = Chat(mm)
    return chat

# def get_info(hm):
#     while True:
#         account = hm.req.get_current_user()
#         queue = Chat.USER_QUEUE_DICT.get(account, {})
#         try:
#             friend = queue.get(timeout=10)  # 10秒后断开, 在连接
#             return 0, {'msg': 'ok', 'data': 'get_page();send_request(url)'}
#         except Exception as e:
#             return 1, {'mes': '没有新消息'}


# def create_thread(hm):
#     mm = hm.mm
#     account = hm.req.get_current_user()
#     print account
#     print Chat.USER_QUEUE_DICT
#     queue = Chat.USER_QUEUE_DICT.get(account)
#     try:
#         friend = queue.get(timeout=10)  # 10秒后断开, 在连接
#         return 0, {'msg': 'ok', 'data': friend}
#     except Exception as e:
#         return 1, {'mes':'没有新消息'}