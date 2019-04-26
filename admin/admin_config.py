# -* coding:utf-8 -*-

import settings


menu_name = [
    ('select', u'数据查询'),
    ('operate', u'运营工具'),
    ('develop', u'开发工具'),
    ('see_data', u'查看数据'),
    ('adminlogs', u'日志记录'),
    ('questionnaire', u'问卷调查'),
    ('manager', u'管理'),
]


select_sort = ['user', 'gwentcard', 'payment', 'long_connection', 'rank', 'user_name', 'other']
operate_sort = ['card', 'hero', 'equip', 'script', 'item', 'commander_part', 'gene', 'approval_payment',
                'gwentcard', 'mail', 'code', 'payment', 'gs', 'user', 'other', 'scroll_msg']
develop_sort = ['config', 'user']
see_data_sort = ['server_overview', 'payment', 'data']
questionnaire_sort = ['questionnaire']
manager_sort = ['gs']
menu_config = {
    'select': {
        'user': [{
            'name': u"用户数据",
            'sub': [
                ('select', u'用户查询', 1),
                ('update', u'用户修改', 0),
                ('reset_guide', u'重置新手引导', 0),
                ('finish_all_guide', u'跳过新手引导', 0),
                ('reset_mission_main', u'重置主线任务', 0),
                ('reset_mission_side', u'重置支线任务', 0),
                ('spend_person', u'查询消费记录', 1),
                ('earn_log', u'钻石获取记录', 1),
                ('user_logging', u'动作记录', 1),
                ('diamond_log', u'钻石记录', 1),
                ('reset_module', u'重置模块', 0),
                ('select_high_ladder', u'查看竞技场', 1),
                ('modify_high_ladder_rank', u'修改竞技场排名', 0),
                ('modify_high_ladder_enemy', u'修改竞技场敌人排名', 0),
                ('ban_user', u'封号', 0),
                ('export', u'导出玩家数据', 0),
            ],
        }],
        'hero': [{
            'name': u"英雄数据",
            'sub': [
                ('select', u'英雄查询', 1),
                ('hero_update', u'修改英雄', 0),
                ('stone_update', u'修改灵魂石', 0)],
        }, {
            'name': u'英雄属性',
            'sub': [('select_attr', u'英雄查询', 1)],
        }],
        'item': [{
            'name': u"道具数据",
            'sub': [
                ('select', u'道具查询', 1),
                ('item_update', u'修改使用道具', 0),
                ('gitem_update', u'修改进阶道具', 0),
                ('citem_update', u'修改采集道具', 0),
                ('ggitem_update', u'修改公会道具', 0),
                ('aitem_update', u'修改觉醒道具', 0)
            ],
        }, {
            'name': u"统帅数据",
            'sub': [
                ('select_commander', u'统帅查询', 1),
                ('commander_update', u'修改统帅', 0)
            ],
        }, {
            'name': u"统帅碎片",
            'sub': [
                ('select_commander_part', u'统帅碎片查询', 1),
                ('commander_part_update', u'修改统帅碎片', 0)
            ],
        }],
        'equip': [{
            'name': u"装备数据",
            'sub': [
                ('select', u'装备查询', 1),
                ('equip_update', u'修改装备', 0)
            ],
        }],
        'gene': [{
            'name': u"基因数据",
            'sub': [
                ('select', u'基因查询', 1),
                ('gene_update', u'修改基因', 0)
            ],
        }],
        'private_city': [{
            'name': u"关卡数据",
            'sub': [
                ('select', u'关卡查询', 1),
                ('clearance', u'关卡通关', 0),
                ('update', u'修改关卡数据', 0)
            ],
        }],
        # 'gwentcard': [{
        #     'name': u"昆特牌数据",
        #     'sub': [('select', u'昆特牌查询', 1), ('gwent_card_update', u'修改昆特牌', 1)],
        # }],
        # 'spend': [{
        #     'name': u"查询消费记录",
        #     'sub': [('spend_person', u'查询消费记录', 1)],
        # }],
        # 'long_connection': [{
        #     'name': u"查询长连数据",
        #     'sub': [('index', u'查询长连数据', 1)],
        # }],
        'mail': [{
            'name': u"查询邮件",
            'sub': [
                ('select', u'查询邮件', 1),
                ('mail_update', u'更新邮件', 0)
            ],
        }],
        'rank': [{
            'name': u"查询排行榜",
            'sub': [
                ('select', u'查询排行榜', 1),
            ],
        }],
        'user_name': [{
            'name': u"查询名字",
            'sub': [
                ('select_name', u'查询邮件', 1)
            ],
        }],
        'other': [{
            'name': u"查询聊天数据",
            'sub': [
                ('select_chat_data', u'查询聊天数据', 1),
                ('delete_chat_data', u'删除聊天数据', 0)
            ],
        },{
            'name': u"查询弹幕",
            'sub': [
                ('select_danmu_data', u'查询弹幕数据', 1),
                ('delete_danmu_data', u'删除弹幕数据', 0)
            ],
        }],
    },
    'operate': {
        'card': [{
            'name': u"送卡牌",
            'sub': [('add_card', u'赠送卡牌', 0)],
        }, {
            'name': u"送卡牌碎片",
            'sub': [('add_piece', u'赠送卡牌碎片', 0)],
        }],
        'item': [{
            'name': u"送道具",
            'sub': [('add_item', u'赠送道具', 0)],
        },
        #     {
        #     'name': u"送进阶道具",
        #     'sub': [('add_gitem', u'赠送进阶道具', 0)],
        # },
        #     {
        #     'name': u"送队长技能",
        #     'sub': [('add_leader_skill', u'送队长技能', 0)],
        # },
        #     {
        #     'name': u"送公会礼物道具",
        #     'sub': [('add_ggitem', u'赠送公会礼物道具', 0)],
        # },
        #     {
        #     'name': u"送觉醒道具",
        #     'sub': [('add_aitem', u'赠送觉醒道具', 0)],
        # }, {
        #     'name': u"送统帅碎片",
        #     'sub': [('add_commander_part', u'赠统帅碎片', 0)],
        # }
        ],
        'equip': [{
            'name': u"送装备",
            'sub': [('add_equip', u'赠送装备', 0)],
        },
            {
                'name': u"送装备碎片",
                'sub': [('add_piece', u'赠送装备碎片', 0)],
            }

        ],
        'script': [
            {'name': u'送剧本', 'sub': [('add_script', u'赠送剧本 ', 0)]},
        ],
        # 'gene': [{
        #     'name': u"送基因",
        #     'sub': [('add_gene', u'赠送基因', 0)],
        # }],
        # 'gwentcard': [{
        #     'name': u"送昆特牌",
        #     'sub': [('add_gcard', u'赠送昆特牌', 0)],
        # }],
        'payment': [{
            'name': u"虚拟充值",
            'sub': [
                ('select_virtual', u'虚拟充值页', 1),
                ('virtual_pay', u'提交虚拟充值', 0)
            ],
        }],
        'approval_payment': [{
            'name': u"充值审批",
            'sub': [
                ('approval_index', u'充值审批', 1),
                ('for_approval', u'进行审批', 0),
            ],
        },{
            'name': u"充值审批查询",
            'sub': [('search_approval', u'充值审批查询', 1)],
        }],
        'gs': [{
            'name': u"客服",
            'sub': [
                ('game_service', u'客服', 1),
                ('send_gs_notify', u'客服回复', 1)
            ],
        }],
        'user': [{
            'name': u"封号记录",
            'sub': [('watch_ban_uids', u'封号记录', 1)],
        },{
            'name': u"封ip记录",
            'sub': [('watch_ban_ips', u'封ip记录', 1), ('ban_ip', u'封ip', 0)],
        }],
        'mail': [{
            'name': u"发送系统邮件",
            'sub': [('add_mail', u'发送系统邮件', 0)],
        }],
        # 'other': [{
        #     'name': u'斗技卡牌使用记录',
        #     'sub': [('king_war_hero_use_info', u'斗技卡牌使用记录', 1)],
        # }],
        'scroll_msg': [{
            'name': u'跑马灯信息',
            'sub': [('scroll_msg', u'跑马灯信息', 1)],
        }],
        'code': [{
            'name': u"激活码",
            'sub': [
                ('code_index', u'激活码', 1),
                ('code_show', u'显示激活码', 1),
                ('code_history', u'历史生成次数', 1),
                ('code_create', u'生成激活码', 0)
            ],
        }],
    },
    'develop': {
        'config': [{
            'name': u"后端配置",
            'sub': [
                ('select', u'后端配置首页', 1),
                ('upload', u'配置上传', 1),
                ('refresh', u'配置更新', 1)
            ],
        },
        #     {
        #     'name': u"前端配置",
        #     'sub': [('front_select', u'前端配置首页', 1)],
        # },
            {
            'name': u"配置下载",
            'sub': [('get_deploy', u'配置下载首页', 1), ('deploy_download', u'配置下载', 1)],
        },{
            'name': u"区服配置",
            'sub': [
                ('server_list', u'区服配置列表', 1),
                ('server_change', u'区服配置修改', 0)
            ],
        },{
            'name': u"修改时间",
            'sub': [
                ('modify_time_index', u'修改时间首页', 1),
                ('modify_time', u'修改时间', 1)],
        }],
    },
    'adminlogs': {
        'adminlogs': [{
            'name': u"日志查询",
            'sub': [('adminlog_index', '查询近期所有日志', 1),
                    ('adminlog_search_by_name', '按名字搜索', 1),
                    ('adminlog_search_by_time', '按日期搜索', 1)],
        }],
        'idea': [{
            'name': u"玩家建议",
            'sub': [('idea_index', '查询玩家建议', 1),]
        }],
    },
    'see_data': {
        'server_overview': [{
            'name': u'充值及在线总数',
            'sub': [('select', u'充值及在线查询', 1)],
        }],
        'payment': [{
            'name': u"充值详情",
            'sub': [('select_pay', u'查询充值记录', 1), ('pay_day', u'查询某天的充值', 1),
                    ('pay_person', u'查询某人的充值', 1)],
        }],
        'data': [
            {
                'name': u'查看定时任务',
                'sub': [
                    ('show_run_timer_jobs', u'查看定时任务', 1)
                ]
            },
            {
            'name': u"数据统计[uid]",
            'sub': [
                ('statistics_index', u'数据统计[uid]', 1),
                ('statistics_channel', u'数据统计[uid]渠道统计', 1),
            ]
        }, {
            'name': u"留存统计[uid]",
            'sub': [
                ('retention_index', u'留存统计[uid]', 1),
                ('retention_channel', u'留存统计[uid]渠道统计', 1),
            ]
        }, {
            'name': u"数据统计[account]",
            'sub': [
                ('statistics_index_account', u'数据统计[account]', 1),
                ('statistics_channel_for_one', u'数据统计[account]单渠道统计', 1),
            ]
        }, {
            'name': u"留存统计[account]",
            'sub': [
                ('retention_index_account', u'留存统计[account]', 1),
                ('retention_index_account', u'留存统计[account]', 1),
            ]
        },
            {
                'name': u"留存统计[device]",
                'sub': [
                    ('retention_index_device', u'留存统计[device]', 1),
                ]
            },
            {
                'name': u"LTV统计[device]",
                'sub': [
                    ('ltv_index_device', u'LTV统计[device]', 1),
                ]
            },

            {
            'name': u"等级滞留统计",
            'sub': [('lv_pass_rate_index', u'等级滞留统计', 1)]
        }, {
            'name': u"查看世界boss排行",
            'sub': [('world_boss_rank_show', u'查看世界boss排行', 1)]
        },
            # {
            #     'name': u'slg在线统计',
            #     'sub': [('slg_status', u'slg在线统计', 1)]
            # }
        ],
    },
    'questionnaire': {
        'questionnaire': [{
            'name': u'问卷调查',
            'sub': [('select', u'问卷调查', 0), ('commit', u'提交问卷', 0)],
        },{
            'name': u'查询问卷',
            'sub': [('find', u'查询问卷', 0)],
        }],
    },
    'manager': {
        'gs': [{
            'name': u"账号管理",
            'sub': [('select', u'账号管理', 0), ('gs_admin', u'查看一个账号', 0),
                    ('modify_admin', u'修改权限', 0), ('delete_admin', u'删除管理员', 0)],
        },{
            'name': u"增加账号",
            'sub': [('add_admin', u'增加账号', 0)],
        },{
            'name': u"修改密码",
            'sub': [('change_password', u'修改密码', 1)],
        },{
            'name': u"退出",
            'sub': [('logout', u'退出', 1)],
        }],
    },
}
