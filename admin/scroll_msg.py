#! --*-- coding: utf-8 --*--


from admin import render
from models.server import ServerConfig

def scroll_msg(req):
    result = {'msg': '', 'content': '', 'server': ''}
    if req.request.method == 'POST':
        server = req.get_argument('server', '')
        if not server:
            result['msg'] = 'server is not empty'
            return render(req, 'admin/scroll_msg/scroll_msg.html', **result)
        content = req.get_argument('content', '')

        data = {
            'message_id': '',
            'uid': '',
            'name': '',
            'target1': '',
            'target2': '',
            'hero_id': '',
            'equip_id': '',
            'arena_rank': '',
        }
        data['msg'] = content
        from chat.to_server import send_to_all
        if server == 'all':
            server_list = [i['server'] for i in ServerConfig.get().server_list()]
        elif ',' in server:
            server_list = server.split(',')
        else:
            server_list = [server]
        content = ''
        for server in server_list:
            try:
                send_to_all(data, server)
                content = content + '%s成功'%server
            except:
                print 'scroll_bar send msg err'
                content = content + '%s失败'%server
        result['server'] = server
        result['content'] = content
    render(req, 'admin/scroll_msg/scroll_msg.html', **result)
