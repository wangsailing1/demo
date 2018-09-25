# -*- coding: utf-8 –*-
import settings
from gconfig import game_config
from models.ranking_list import OutPutRank
import time
from lib.utils.debug import print_log


def send_output_reward(server):
    from lib.core.environ import ModelManager
    if not settings.is_father_server(server):
        return
    config = game_config.out_put_reward
    output_rank = OutPutRank('', server)
    output_rank_list = output_rank.get_all_user(withscores=True)
    if not output_rank_list:
        return
    for rank, value in enumerate(output_rank_list, 1):
        if rank not in config:
            continue
        gift = config[rank]['reward']
        uid_script, score = value
        uid, script = uid_script.split('|')
        mm = ModelManager(uid)
        des = ''
        title = 'output_reward'
        mail_dict = mm.mail.generate_mail(des, title=title, gift=gift)
        mm.mail.add_mail(mail_dict)
        mm.mail.save()

    output_rank_list.delete()
    print_log(time.strftime('%F'), 'send_output_reward done')
