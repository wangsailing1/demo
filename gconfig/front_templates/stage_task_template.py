#! --*-- coding: utf-8 --*--

__author__ = 'kaiqigu'

# 活动相关的配置
from gconfig import check


stage_task_main = {
    'uk': ('sort', 'int'),                  # 主题
    'start_time': ('start_time', 'int'),    # 开启时间
    'length': ('length', 'int'),            # 持续时间
    'task_num': ('task_num', 'int'),        # 领取大奖需要完成任务数
    'reward': ('reward', 'list_3', check.check_reward()),   # 大奖
    'banner': ('banner', 'str'),            # 大奖banner图标
    'task_id': ('task_id', 'int_list'),     # 任务id
    'des': ('des', 'unicode'),              # 目标描述
    'anim': ('anim', 'str'),                # 动画
    'name': ('name', 'unicode'),
}


stage_task_details = {
    'uk': ('id', 'int'),
    'open_day': ('open_day', 'int'),        # 第x天开启
    'act1_name': ('act1_name', 'unicode'),  # 大任务1名称
    'act1_id': ('act1_id', 'int_list'),     # 大任务1id
    'act2_name': ('act2_name', 'unicode'),  # 大任务2名称
    'act2_id': ('act2_id', 'int_list'),     # 大任务2id
    'act3_name': ('act3_name', 'unicode'),  # 大任务3名称
    'act3_id': ('act3_id', 'int_list'),     # 大任务3id
    'act4_name': ('act4_name', 'unicode'),  # 大任务4名称
    'act4_id': ('act4_id', 'int_list'),     # 大任务4id
}


stage_task_info = {
    'uk': ('id', 'int'),
    'sort': ('sort', 'int'),                # 任务类型
    'target1': ('target1', 'int'),    # 目标1
    'target2': ('target2', 'int'),    # 目标2
    'reward': ('reward', 'list_3'),         # 奖励
    'des': ('des', 'unicode'),              # 目标描述
    'jump': ('jump', 'int'),                # 跳转
    'is_count': ('is_count', 'int'),        # 是否显示计数
}
