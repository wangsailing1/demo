#! --*-- coding: utf-8 --*--

__author__ = 'sm'

# 道具相关的配置
from gconfig import check


# 英雄进阶徽章材料
grade_lvlup_item = {
    'uk': ('id', 'int'),  # 徽章id
    'sort': ('sort', 'int'),  # 类型
    'name': ('name', 'unicode'),  # 徽章名字
    'icon': ('icon', 'str'),   # 徽章icon
    'quality': ('quality', 'int'),  # 徽章品质
    'story': ('story', 'unicode'),  # 描述
    'lv': ('lv', 'int'),  # 佩戴等级
    'effect': ((('hp', 'hp'),  # 徽章效果
              ('phy_atk', 'phy_atk'),
              ('phy_def', 'phy_def'),
              ('mag_atk', 'mag_atk'),
              ('mag_def', 'mag_def')), ('float', 'mult_key_dict')),
    'price': ('price', 'int'),  # 徽章出售价格
    'guide': ('guide', 'list_int_list'),  # 掉落指引
}


# 普通道具表
# 0:不可使用
# 1：宝箱
# 2：增加金币
# 3：增加道具
# 4：增加进阶材料
# 5：增加采集物
# 6：增加装备
# 7：增加经验（不可使用，只能在英雄升级页面被动使用）"
# 根据is_use填写
# 0：不填
# 1：box_id
# 2：数值
# 3：道具ID，数量
# 4：材料ID，数量
# 5：采集物ID，数量
# 6：装备ID，数量
# 7：数值"
use_item = {
    'uk': ('id', 'int'),  # 道具id
    'type': ('type', 'int'),  # 类型
    'name': ('name', 'unicode'),  # 名字
    'story': ('story', 'unicode'),  # 说明
    'icon': ('icon', 'str'),   # icon
    'quality': ('quality', 'int'),   # 品质
    'star': ('star', 'int'),   # 星级
    'is_use': ('is_use', 'int'),   # 使用类型
    'use_effect': ('use_effect', 'use_item'),   # 使用效果
    'guide': ('guide', 'int_list_or_int'),   # 掉落
    'is_piece': ('is_piece', 'int'),    # 是否为碎片
    'use_num': ('use_num', 'int'),      # 碎片合成需要的数量
}


# 宝箱
use_item_box = {
    'uk': ('box_id', 'int'),        # 道具id
    'use_lv': ('use_lv', 'int'),    # 使用等级
    'use_times': ('use_times', 'int'),      # 使用次数
    'sort': ('sort', 'int'),        # 宝箱类型
    'effect': ('effect', 'int_float_list_or_int_float'),    # 与sort对应
    'story': (('reward1', 'num1', 'level1', 'reward2', 'num2', 'level2',
               'reward3', 'num3', 'level3', 'reward4', 'num4', 'level4',
               'reward5', 'num5', 'level5', 'reward6', 'num6', 'level6',
               'reward7', 'num7', 'level7', 'reward8', 'num8', 'level8',
               'reward9', 'num9', 'level9', 'reward10', 'num10', 'level10',), ('', 'use_item_box')),  # 说明
}


# 资源配置
collection_resource = {
    'uk': ('id', 'int'),  # 资源id
    'sort': ('sort', 'int'),  # 类型 1：铁矿  2：木材  3：皮革
    'exchange_type': ('exchange_type', 'int'),  # 合成分类 1：铁矿  2：木材  3：皮革 4: 稀有铁矿 5: 稀有木材 6: 稀有皮革
    'name': ('name', 'unicode'),  # 名字
    'type': ('type', 'int'),  # 是否可指定采集 0：不可指定，1：可指定
    'lv': ('lv', 'int'),   # 资源等阶
    'if_exchange': ('if_exchange', 'int'),  # 是否可用于合成
    'collection_value': ('collection_value', 'int'),   # 采集能力
    'icon': ('icon', 'str'),   # icon
    'quality': ('quality', 'int'),   # 品质框
    'weight': ('weight', 'int'),   # 采集权重
    'story': ('story', 'unicode'),   # 物品描述
}

# 特殊使用类道具
special_use_item = {
    'uk': ('id', 'int'),                        # 编号
    'sort': ('sort', 'int'),                    # 类型 1:装备, 2:英雄
    'use_item_id': ('use_item_id', 'int'),      # 物品id
    'evo': ('evo', 'int'),                      # 物品档次
    'lvl': ('lvl', 'int'),                      # 基因等级/英雄等级
    'star': ('star', 'int'),                    # 星级
}
