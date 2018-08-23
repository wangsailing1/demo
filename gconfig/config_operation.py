#! --*-- coding: utf-8 --*--

# 要拆分的表{表名：拆分成多少个表}
RESOLVE_LIST = {
    'ZH_CN': 10,
    'ZH_TW': 10,
}


# def fake_tech_tree(config):
#     """
#     生成科技树假配置
#     :param config:
#     :return:
#     """
#     tech_tree_mapping = {"G": [], "P": [], "D": []}  # 两种特殊装备需要不同的材料升级
#     dot_num = len(config.keys())
#     b = 999  # 替代正无穷
#     t = 0
#     if dot_num:
#         # 初始矩阵
#         for i in xrange(dot_num):
#             p_list = [0] * dot_num
#             g_list = [b] * dot_num
#             tech_tree_mapping["P"].append(list(p_list))
#             tech_tree_mapping["G"].append(g_list)
#         for i in xrange(dot_num):
#             for j in xrange(dot_num):
#                 if i == j:
#                     tech_tree_mapping["G"][i][j] = t
#                 elif j in config[i]['link']:
#                     tech_tree_mapping["G"][i][j] = 1
#                 else:
#                     tech_tree_mapping["G"][i][j] = b
#         # 计算后的的矩阵
#         copy_tech_tree_mapping = tech_tree_mapping
#         length = len(copy_tech_tree_mapping["G"])
#         # TODO 是否需要引用
#         copy_tech_tree_mapping["D"] = copy_tech_tree_mapping['G']
#
#         for u in xrange(0, length):
#             for s in xrange(0, length):
#                 # 会修改config
#                 copy_tech_tree_mapping["P"][u][s] = s
#         for k in xrange(0, length):
#             D_k = copy_tech_tree_mapping["D"][k]
#             for v in xrange(0, length):
#                 D_v = copy_tech_tree_mapping["D"][v]  # list
#                 P_v = copy_tech_tree_mapping["P"][v]
#                 for w in xrange(0, length):
#                     if D_v[w] > D_v[k] + D_k[w]:
#                         D_v[w] = D_v[k] + D_k[w]
#                         P_v[w] = P_v[k]
#
#         copy_tech_tree_mapping.pop('G')
#         return [['tech_tree_D', copy_tech_tree_mapping['D']], ['tech_tree_P', copy_tech_tree_mapping['P']]]
#     return [['tech_tree_D', {}], ['tech_tree_P', {}]]


# 生成假配置
FAKE_CONFIG = {
    # 根据那个配置生成假配置           生成假配置的函数该函数返回配置名及配置            假配置名的列表                          后端1，前端2
    # 'tech_tree':                    [fake_tech_tree,                            ['tech_tree_D', 'tech_tree_P'],      [1, 2]],
}

