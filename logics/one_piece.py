# -*- coding: utf-8 -*-

__author__ = 'ljm'

import time
import datetime
import itertools
import random
import cPickle as pickle
import copy

import settings
from gconfig import game_config
from lib.utils import weight_choice
from lib.utils.active_inreview_tools import active_inreview_version
from lib.utils.active_inreview_tools import active_inreview_start_end_time
from lib.utils.active_inreview_tools import format_time_active_version
from tools.gift import add_mult_gift, add_gift_by_weights
from lib.utils.debug import print_log
from lib.core.environ import ModelManager


class OnePieceLogic(object):
    def __init__(self, mm):
        """
        """
        self.mm = mm
        self.one_piece = self.mm.one_piece
        self.one_piece_config = copy.deepcopy(game_config.one_piece.get(self.one_piece.version, {}))
        self.one_piece_config['start_time'] = game_config.active.get(self.one_piece.config_id,{}).get('start_time','')
        self.one_piece_config['end_time'] = game_config.active.get(self.one_piece.config_id,{}).get('end_time','')

    def index(self):
        rank = self.one_piece.get_rank()
        data = {
            'version': self.one_piece.version,           # 当前版本号
            'score': self.one_piece.times,               # 次数
            'rank': rank,                               # 排名
            'key_num': self.mm.item.get_item(self.one_piece.KEY_ID),       # 钥匙的数量
            'open_times': self.one_piece.get_remain_free_times(),                    # 开启次数
            'remainder_time': self.get_remain_time(),               # 活动剩余时间
            'step_reward': self.one_piece.step_reward,              # 阶段奖励领取数据
            'exchange_index': self.exchange_index(),
            'show_ranking': self.one_piece_config.get('show_ranking', 0),       # 是否显示开服时间
        }

        return data

    def is_open(self):
        """  是否开启

        :return:
        """
        return True if self.one_piece.is_open(self.one_piece_config) else False

    def info(self):
        """ 获取信息

        :return:
        """
        rank_info = self.get_score_rank_info()
        return {'rank_info': rank_info,
                'version':self.one_piece.version
                }

    def is_show_rank(self):
        """ 是否展示排行

        :return:
        """
        return True if self.one_piece_config.get('show_ranking', 0) != 0 else False

    def get_remain_time(self):
        """ 获取剩余时间

        :return:
        """
        version = active_inreview_version(game_config.active,active_id=self.one_piece.ACTIVE_ID)
        if version and self.one_piece.version != version:
            return 0
        if self.one_piece_config:
            end_time = self.one_piece_config['end_time']
            end_time = time.mktime(time.strptime(end_time, self.one_piece.TIME_FORMAT))
            return max(int(end_time - time.time()), 0)
        return 0

    def open_roulette(self):
        """ 开启轮盘

        :return:
        """
        is_save_user = False
        if self.one_piece.get_remain_free_times() <= 0:
            # 次数不足需要花费钻石
            price = self.one_piece_config.get('one_coin', 48)
            if not self.mm.user.is_diamond_enough(price):
                return 'error_4', {}

            self.mm.user.deduct_diamond(price)
            is_save_user = True

            # 获取宝箱
            one_piece_rate_id, gifts = self.receive_random_gifts()
            reward = add_mult_gift(self.mm, gifts)
            if one_piece_rate_id in self.one_piece.score:
                self.one_piece.score[one_piece_rate_id] = max(0, self.one_piece.score[one_piece_rate_id] - self.one_piece_config['max_score'])
            self.add_score(save=False)
        else:
            # 扣除次数
            self.one_piece.open_times += 1

            # 获取免费宝箱
            # print self.one_piece_config
            free_reward = self.one_piece_config['free_reward']
            _gift_config = weight_choice(free_reward)
            gifts = copy.deepcopy([_gift_config[:3]])
            reward = add_mult_gift(self.mm, gifts)
            one_piece_rate_id = random.randint(5, 8)

        # 伪随机
        self.one_piece.incrby_pro(1)

        # 更新排行榜
        self.one_piece.update_key(1, save=False)

        gift = [[5, self.one_piece.KEY_ID, 1]]
        reward = add_mult_gift(self.mm, gift, reward)

        gifts.extend(gift)

        self.one_piece.save()
        if is_save_user:
            self.mm.user.save()

        result = {
            'reward': reward,
            'gifts': gifts,
            'index': one_piece_rate_id,
        }
        result.update(self.index())

        return 0, result

    def open_roulette10(self):
        """ 开启轮盘10次

        :return:
        """
        price = self.one_piece_config.get('ten_coin', 480)
        if not self.mm.user.is_diamond_enough(price):
            return 'error_4', {}

        self.mm.user.deduct_diamond(price)

        reward = {}
        index = None

        gifts = [[5, self.one_piece.KEY_ID, 11]]

        for i in xrange(11):
            one_piece_rate_id, gift = self.receive_random_gifts()
            if index is None:
                index = one_piece_rate_id
            if one_piece_rate_id in self.one_piece.score:
                self.one_piece.score[one_piece_rate_id] = max(0, self.one_piece.score[one_piece_rate_id] - self.one_piece_config['max_score'])

            gifts.extend(gift)

        self.add_score(num=11, save=False)

        reward = add_mult_gift(self.mm, gifts, reward)

        # 伪随机
        self.one_piece.incrby_pro(11)

        # 更新排行榜
        self.one_piece.update_key(11, save=False)

        self.mm.user.save()

        self.one_piece.save()

        result = {
            'reward': reward,
            'gifts': gifts,
            'index': index,
        }
        result.update(self.index())

        return 0, result

    def receive_random_gifts(self):
        """ 领取奖励

        :return:
        """
        # one_piece_rate_config = game_config.one_piece_rate
        one_piece_rate_config = {}
        for active_id, value in game_config.one_piece_rate.iteritems():
            if value.get('version') == self.one_piece.version:
                one_piece_rate_config[value.get('id')] = value
        if not one_piece_rate_config:
            return
        one_piece_rate_config = pickle.loads(pickle.dumps(one_piece_rate_config))
        # 获取id的最小值加上10000
        one_piece_rate_id = min(one_piece_rate_config)
        max_score = self.one_piece_config['max_score']
        max_rate = self.one_piece_config['max_rate']
        index, is_server = self.is_server_score()
        if is_server:
            if one_piece_rate_id not in self.one_piece.score:
                self.one_piece.score[one_piece_rate_id] = max_score
            else:
                self.one_piece.score[one_piece_rate_id] += max_score
            self.one_piece.update_status(index)
        special_rewards = []
        for i, score in self.one_piece.score.iteritems():
            if score >= max_score and i in one_piece_rate_config:
                special_rewards.append([i, one_piece_rate_config[i]['reward'], max_rate])

        special_rewards.sort(key=lambda x: x[0])

        if special_rewards:
            reward = [special_rewards[0]]
        else:
            reward = []

        for k, v in one_piece_rate_config.iteritems():
            rate = v['rate']
            if rate:
                if special_rewards:
                    reward.append([k, v['reward'], rate * 0.2])
                else:
                    reward.append([k, v['reward'], rate])

        result = weight_choice(reward)[:2]

        return copy.deepcopy(result)

    def is_server_score(self):
        """ 是否满足全服积分需求

        :return:
        """
        vip_limit = self.one_piece_config['vip_limit']
        if self.mm.user.company_vip > vip_limit:
            return -1, False
        server_score = self.one_piece_config['server_score']
        pro_data = self.one_piece.get_pro_data()
        pro_num = int(pro_data.get('score',0))
        if not pro_num:
            return -1, False
        pro_status = int(pro_data.get('status', -1))
        for i, score in enumerate(server_score):
            if i <= pro_status:
                continue
            if pro_num < score:
                return -1, False
            if pro_num >= score:
                return i, True

        return -1, False

    def add_score(self, num=1, save=True):
        """ 增加积分

        :return:
        """
        for k, v in game_config.one_piece_rate.iteritems():
            if v.get('version') != self.one_piece.version:
                continue
            score_config = v['score']
            if not score_config:
                continue

            if v['has_reduce']:
                score_config = score_config * self.get_vip_rate() / 100.0
            key = v['id']
            if key not in self.one_piece.score:
                self.one_piece.score[key] = score_config * num
            else:
                self.one_piece.score[key] += score_config * num

        if save:
            self.one_piece.save()

    def get_score_rank_info(self, start=1, end=50):
        """ 获取积分排行榜信息

        :return:
        """
        from models.user import User as UserM

        ranks = self.one_piece.get_score_ranks(start=start, end=end)

        score_ranks = []
        for (uid, score), rank in itertools.izip(ranks, xrange(start, end + 1)):
            u = UserM.get(uid)
            score_ranks.append(dict(uid=u.uid, name=u.name, score=score))

        return score_ranks

    def get_active_day(self):
        """ 获取活动的天数

        :return:
        """
        start_time = self.one_piece_config.get('start_time',0)
        open_time = datetime.datetime.strptime(start_time, self.one_piece.TIME_FORMAT)
        now = datetime.datetime.now().date()
        diff_day = now - open_time.date()
        return diff_day.days + 1

    def get_vip_rate(self):
        """ 获取vip几率

        :return:
        """
        config = game_config.one_piece_reduce.get(self.mm.user.company_vip, {})
        if not config:
            return 50
        days = self.get_active_day()
        return config.get('day_%s' % days, 50)

    def exchange_index(self):
        """ 兑换首页 1.表示固定

        :return:
        """
        result = {'exchange_1': {}, 'exchange_2': {}}
        global_data = self.one_piece.get_all_global_data()
        for k, v in game_config.one_piece_exchange.iteritems():
            if v.get('version') == self.one_piece.version:
                limit_num = v.get('limit_num', 0)
                sort = v['sort']
                if sort == 1:
                    show = result['exchange_1']
                else:
                    show = result['exchange_2']
                if limit_num:
                    if sort in {1, 2}:
                        remain = limit_num - self.one_piece.goods.get(k, 0)
                        if remain <= 0:
                            continue
                        show[k] = {'remain': remain}
                    else:
                        show[k] = {'remain': limit_num - int(global_data.get(str(k), 0))}
                else:
                    show[k] = {'remain': -1}

        return {'gifts': result}

    def exchange(self, exchange_id):
        """ 兑换接口
            1. 钥匙不足
            2. 没有可兑换的物品
            3. 物品数值不足
        :return:
        """
        config = {}
        for k, value in game_config.one_piece_exchange.iteritems():
            if value.get('version') == self.one_piece.version and k == exchange_id:
                config = game_config.one_piece_exchange.get(exchange_id)

        if not config:
            return 2, {}

        need_key_num = config.get('need_key_num', 100000)

        count = self.mm.item.get_item(self.one_piece.KEY_ID)

        if need_key_num > count:
            return 1, {}

        limit_num = config.get('limit_num', 0)
        player_limit = config.get('player_limit',0)

        if limit_num or player_limit:
            if config['sort'] in {1, 2}:
                remain = limit_num - self.one_piece.goods.get(exchange_id, 0)
                if remain <= 0:
                    return 3, {}
                if exchange_id not in self.one_piece.goods:
                    self.one_piece.goods[exchange_id] = 1
                else:
                    self.one_piece.goods[exchange_id] += 1
                self.one_piece.save()
            else:
                remain1 = limit_num - self.one_piece.get_global_data(exchange_id)
                remain2 = player_limit - self.one_piece.goods.get(exchange_id, 0)
                if remain1 <= 0 or (player_limit and remain2 <= 0):
                    return 3, {}
                if limit_num:
                    self.one_piece.incrby_global(exchange_id)
                if player_limit:
                    if exchange_id not in self.one_piece.goods:
                        self.one_piece.goods[exchange_id] = 1
                    else:
                        self.one_piece.goods[exchange_id] += 1
                    self.one_piece.save()

        gifts = config.get('reward', [])
        reward = add_mult_gift(self.mm, gifts)

        self.mm.item.del_item(self.one_piece.KEY_ID, need_key_num)
        self.mm.item.save()

        return 0, {'reward': reward}

    def step_reward(self, step):
        """ 阶段奖励
            1. 领取过
            2. 没有该奖励
            3. 积分不足
        :param step:
        :return:
        """
        if step in self.one_piece.step_reward:
            return 1, {}

        score = self.one_piece_config.get('score')[step - 1]

        if score is None:
            return 2, {}

        if self.one_piece.times < score:
            print self.one_piece.times, score
            return 3, {}

        gifts = self.one_piece_config.get('reward')[step - 1]

        reward = add_mult_gift(self.mm, gifts)

        self.one_piece.step_reward.append(step)
        self.one_piece.save()

        return 0, {'reward': reward}


def refresh_one_piece(server, differ_time = 3600*4):
    """ 刷新

    :param server:
    :return:
    """
    if not settings.is_father_server(server):
        return None

    from lib.db import ModelBase
    from models.one_piece import OnePiece as OnePieceModel
    from logics.user import UserLogic
    key = ModelBase.make_key_cls('refresh_one_piece_flag', server)
    _client = ModelBase.get_redis_client(key, server)
    db_start_time = _client.get(key)

    if not game_config.one_piece_rank_reward:
        return

    version = format_time_active_version(game_config.one_piece, '%Y/%m/%d %H:%M:%S', differ_time)

    if not version:
        return

    rm = OnePieceModel()
    # one_id = max(game_config.one_piece_rank_reward)
    one_list = []
    for id, value in game_config.one_piece_rank_reward.iteritems():
        if value.get('version') == version:
            one_list.append(id)
    one_id = max(one_list)
    reward_time = game_config.one_piece_rank_reward[one_id]['reward_time']

    if db_start_time and db_start_time == reward_time:
        return

    result = {
        'db_start_time': db_start_time,
        'max_version': version,
        'reward': [],
    }

    # max_version = max(game_config.one_piece)
    # version = active_inreview_start_end_time(game_config.one_piece_rank_reward)
    rank_key = rm.get_rank_key(server, version)
    rm.rank_db = rm.get_redis_client(server)

    for indx, value in game_config.one_piece_rank_reward.iteritems():
        if value.get('version') == version:
            start_rank, end_rank = value['rank']
            data = rm.get_score_ranks(start_rank, end_rank)
            for (uid, score), rank in itertools.izip(data, xrange(start_rank, end_rank+1)):
                mm = ModelManager(uid)
                # todo 取邮件内容
                content = value['mail'] % {'rank': rank}
                message = mm.mail.generate_mail(unicode('one_piece_rank_reward', 'utf-8'), content, value['rank_reward'])
                mm.mail.add_mail(message, save=True)
                result['reward'].append({'uid': uid, 'score': score, 'rank': rank, 'indx': indx})

    # 藏宝图结束后脚本发奖时，把未领取的阶段奖励替玩家自动领取

    uid_list = rm.get_score_ranks(1, 0)
    for uid, score in uid_list:
        try:
            mm = ModelManager(uid)
        except:
            continue

        OP_instance = OnePieceLogic(mm)

        for i in xrange(1, 4):                      # 藏宝图策划规定的积分奖励有三档，如果以后变动的话，此处要修改
            step_reward_result = OP_instance.step_reward(i)

    # 阶段奖励自动领取代码段结束


    rm.rank_db.delete(rank_key)
    pro_key = rm.get_pro_key(server, version)
    rm.rank_db.delete(pro_key)
    global_key = rm.get_global_key(server, version)
    rm.rank_db.delete(global_key)

    _client.set(key, reward_time)
    print_log(result)

    return result
