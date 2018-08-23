#! --*-- coding: utf-8 --*--

__author__ = 'sm'

import requests
import json
import urllib

api_url = 'http://127.0.0.1:7001/api/?method=%(method)s&user_token=%(user_token)s'
login_url = 'http://127.0.0.1:7001/login/?method=%(method)s'
config_url = 'http://127.0.0.1:7001/config/?method=%(method)s'

mapping = {
    'account_register': (login_url, 'register', 'account', 'passwd'),
    'account_login': (login_url, 'login', 'account', 'passwd'),
    'account_platform_access': (login_url, 'platform_access', 'pre_pf', 'channel'),
    'user_main': (api_url, 'user.main'),
    'user_game_info': (api_url, 'user.game_info'),
    'guild_guild_all': (api_url, 'guild.guild_all', 'page'),
    'guild_create_guild': (api_url, 'guild.create_guild', 'name', 'icon'),
    'guild_apply_guild': (api_url, 'guild.apply_guild', 'gid'),
    'guild_search_guild': (api_url, 'guild.search_guild', 'name'),
    'guild_remove_player': (api_url, 'guild.remove_player', 'uid'),
    'guild_manage_position': (api_url, 'guild.manage_position', 'vp'),
    'guild_modify_icon': (api_url, 'guild.modify_icon', 'icon'),
    'guild_modify_name': (api_url, 'guild.modify_name', 'name'),
    'guild_exit_guild': (api_url, 'guild.exit_guild'),
    'guild_guild_one': (api_url, 'guild.guild_one', 'gid'),
    'guild_guild_detail': (api_url, 'guild.guild_detail'),
    'guild_agree_join': (api_url, 'guild.agree_join', 'uid'),
    'guild_refuse_join': (api_url, 'guild.refuse_join', 'uid'),
    'guild_refuse_all_join': (api_url, 'guild.refuse_all_join'),
    'guild_set_limit': (api_url, 'guild.set_limit', 'apply_status', 'apply_lv'),
    'friend_friends': (api_url, 'friend.friends'),
    'friend_messages': (api_url, 'friend.messages'),
    'friend_search_friend': (api_url, 'friend.search_friend', 'uid'),
    'friend_apply_friend': (api_url, 'friend.apply_friend', 'uid'),
    'friend_agree_friend': (api_url, 'friend.agree_friend', 'uid', 'mid'),
    'friend_refuse_friend': (api_url, 'friend.refuse_friend', 'mid', 'all_mid'),
    'friend_remove_friend': (api_url, 'friend.remove_friend', 'uid'),
    'gacha_diamond_index': (api_url, 'gacha.diamond_index'),
    'gacha_get_gacha': (api_url, 'gacha.get_gacha', 'port', 'g_id'),
    'guild_trade_index': (api_url, 'guild.trade_index'),
    'guild_add_hero': (api_url, 'guild.add_hero', 'hero_oid'),
    'guild_withdraw_hero': (api_url, 'guild.withdraw_hero'),
    'guild_harvest_reward': (api_url, 'guild.harvest_reward'),
}


user_token = None


def init_data(value):
    global user_token

    user_token = value


def handler(command):
    data = mapping[command]

    if data[0] == api_url and command not in ['account_register', 'account_login'] and user_token is None:
        print u"请注册或者登录: 接口: account_register, account_login"
        return
    if data[0] == api_url:
        uri = data[0] % {'method': data[1], 'user_token': user_token}
    else:
        uri = data[0] % {'method': data[1]}
    params = {}
    for param_name in data[2:]:
        param_value = raw_input(u'请输入参数%s: ' % param_name)
        params[param_name] = param_value
    if params:
        uri = '%s&%s' % (uri, urllib.urlencode(params))
    content = requests.get(uri)
    if content.status_code != 200:
        print u"接口报错: ", content.text
        return

    result = content.json()
    status = result['status']
    if status != 0:
        print u"接口返回错误码: %s, 错误消息: %s" % (status, result['msg'])
        return

    if command in ['account_register', 'account_login']:
        init_data(result['data']['user_token'])

    print u"接口返回值", json.dumps((result['data'], result['user_status']), ensure_ascii=False)


if __name__ == '__main__':
    while True:
        command = raw_input(u'请输入命令: ')
        if command in ['exit', 'quit']:
            break
        if command in ['info']:
            print u"命令如下: \n"
            for k, v in sorted(mapping.iteritems()):
                print k, v[2:]
        elif command in mapping:
            handler(command)
        else:
            print u'命令有误'
        print u"-------------------------------"

    print u"程序已经退出"
