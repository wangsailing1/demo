# -*- coding: utf-8 –*-
from models.ranking_list import AllOutPutRank


def rank_list_backup(server):
    output_rank = AllOutPutRank('', server)
    # output_rank_list = output_rank.get_all_user(withscores=True)
    # if not output_rank_list:
    #     return
    output_rank.rank_backup()


    # for rank, value in enumerate(output_rank_list, 1):
    #     if rank not in config:
    #         continue
    #     gift = config[rank]['reward']
    #     uid_script, score = value
    #     uid, script = uid_script.split('|')
    #     mm = ModelManager(uid)
    #     des = ''
    #     title = 'output_reward'
    #     mail_dict = mm.mail.generate_mail(des, title=title, gift=gift)
    #     mm.mail.add_mail(mail_dict)
    #     mm.mail.save()
    #
    # output_rank_list.delete()
    # print_log(time.strftime('%F'), 'send_output_reward done')
