#! --*-- coding: utf-8 --*--
__author__ = 'kaiqigu'

import time

from lib.core.environ import ModelManager
from lib.db import ModelTools
from lib.utils import generate_rank_score, round_float_or_str
import settings
from lib.db import get_redis_client



class AllRank(ModelTools):
    """排名榜

    """

    def __init__(self, uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = settings.get_father_server(server)
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self.fredis = self.get_father_redis(father_server)
        self._last_version_key = '%s_%s' % (self._key, 'last_version')

    def add_rank(self, uid, rank):
        """
        增加排名
        :param uid:
        :param rank:
        :return:
        """
        self.fredis.zadd(self._key, uid, generate_rank_score(rank))

    def incr_rank(self, uid, score):
        """
        增加排名
        :param uid:
        :param score:
        :return:
        """
        self.fredis.zincrby(self._key, uid, int(score))

    def del_rank(self, uid):
        """
        删除排名
        :param uid:
        :return:
        """
        self.fredis.zrem(self._key, uid)

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        """
        获取排名所有玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrevrange(self._key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_rank_user(self, start, end, withscores=False, score_cast_func=round_float_or_str):
        """
        获取指定rank值范围内的玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrangebyscore(self._key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_score(self, uid, score_cast_func=round_float_or_str):
        """
        获取积分
        :param uid:
        :return:
        """
        score = self.fredis.zscore(self._key, uid) or 0
        score = score_cast_func(score)

        return score

    def get_rank(self, uid):
        """
        获取排名
        :param uid:
        :return:
        """
        rank = self.fredis.zrevrank(self._key, uid)
        if rank is None:
            rank = -1

        return rank + 1

    def get_one_uid(self, rank):
        """
        根据排名获取uid
        :param rank:
        :return:
        """
        if rank < 0:
            return ''

        uids = self.get_all_user(rank - 1, rank - 1)
        if not uids:
            return ''

        return uids[0]

    def get_count(self):
        """
        获取人数
        :return:
        """
        return self.fredis.zcard(self._key)

    def delete(self):
        """ 删除key

        :return:
        """
        self.fredis.delete(self._key)

    def rank_backup(self):
        """
        备份当前排名
        :return:
        """
        key_by_date = self.backup_key()
        if self.fredis.exists(self._key):
            self.fredis.zunionstore(key_by_date, {self._key: 1})
            self.fredis.expire(key_by_date, 7 * 24 * 3600)

    def backup_key(self):
        key_by_date = '%s_%s' % (self._key, 'backup')
        return key_by_date

    def get_rank_before(self, uid):
        key_by_date = self.backup_key()
        rank = self.fredis.zrevrank(key_by_date, uid)
        if rank is None:
            rank = -1

        return rank + 1



class AppealRank(AllRank):
    """
    艺人号召力排行
    uid 格式 uid + '|' + group_id 
    """

    def __init__(self, uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = server
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self.fredis = self.get_redis_client(father_server)
    #     super(AllRank, self).__init__()
    #     self.fredis = get_redis_client(settings.public)
    #     self._key = self.make_key(self.__class__.__name__, server_name='master')
    #     date = time.strftime('%F')
    #     self._key_date = '%s_%s' % (self._key, date)


class OutPutRank(AllRank):
    """
    票房排行
    uid 格式 uid
    """


    def __init__(self,uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = server
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self.fredis = self.get_redis_client(father_server)
    #     super(AllRank, self).__init__()
    #     self.fredis = get_redis_client(settings.public)
    #     self._key = self.make_key(self.__class__.__name__, server_name='master')
    #     weekday = time.strftime("%F")
    #     self._key_date = '%s_%s' % (self._key, weekday)


class AllOutPutRank(AllRank):
    """
    总票房排行
    uid 格式 uid + '|' + group_id
    """

    def __init__(self,uid='', server='', date='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = server
        self._key = self.make_key(self.__class__.__name__, server_name=father_server)
        self.fredis = self.get_redis_client(father_server)

    #     super(AllRank, self).__init__()
    #     self.fredis = get_redis_client(settings.public)
    #     self._key = self.make_key(self.__class__.__name__, server_name='master')
    #     weekday = time.strftime("%F")
    #     self._key_date = '%s_%s' % (self._key, weekday)




class GuildTaskRank(AllRank):
    """
    公会boss降临活动排行榜
    """


class LevelRank(AllRank):
    """
    等级排行榜
    """


class CombatRank(AllRank):
    """
    玩家总战力排行榜
    """


class SuperActiveRank(AllRank):
    """宇宙最强排名榜

    """

    def __init__(self, uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        version = kwargs.get('version', 0)
        father_server = settings.get_father_server(server)
        self._key = self.make_key_cls('rank_%s' % version, server_name=father_server)
        self.fredis = self.get_father_redis(father_server)


class HighladderRank(AllRank):
    """
    天梯竞技场排行榜
    """

    def remove_multi_uids(self, uids):
        """
        从竞技场中删除用户 ps:主要是用来删除机器人
        :param uids:
        :return:
        """
        pipe = self.fredis.pipeline()
        for uid in uids:
            pipe.zrem(self._key, uid)
        return pipe.execute()

    def get_multi_uids(self, ranks):
        """
        获取竞技场中多个排名的uid
        :param ranks:
        :return:
        """
        pipe = self.fredis.pipeline()
        for rank in ranks:
            pipe.zrange(self._key, rank - 1, rank - 1)
        uids = pipe.execute()

        return [i[0] for i in uids if i]

    def get_multi_rank(self, uids):
        """
        获取竞技场中多个排名的uid
        :param uids:
        :return:
        """
        pipe = self.fredis.pipeline()
        for uid in uids:
            pipe.zrank(self._key, uid)

        return pipe.execute()

    def get_multi_score(self, uids):
        """
        获取同一竞技场中多个id的积分
        :param uids:
        :return:
        """
        pipe = self.fredis.pipeline()
        for uid in uids:
            pipe.zscore(self._key, uid)

        scores = []
        for i in pipe.execute():
            if i is None:
                score = 0
            else:
                score = i
            scores.append(score)

        return scores

    def set_multi_score(self, multi_item, _client=None):
        """
        交换用户排名
        :param multi_item: {uid: score}
        :param _client:
        :return:
        """
        pipe = self.fredis.pipeline()
        pipe.zadd(self._key, **multi_item)
        pipe.execute()

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str, last_version=False):
        """
        获取排名所有玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        if last_version:
            data = self.fredis.zrange(self._last_version_key, start, end, withscores=withscores,
                                      score_cast_func=score_cast_func)
        else:
            data = self.fredis.zrange(self._key, start, end, withscores=withscores, score_cast_func=score_cast_func)
        return data

    def get_rank(self, uid, last_version=False):
        """
        获取排名
        :param uid:
        :return:
        """
        if last_version:
            rank = self.fredis.zrank(self._last_version_key, uid)
        else:
            rank = self.fredis.zrank(self._key, uid)
        if rank is None:
            rank = -1

        return rank + 1

    def get_score(self, uid, score_cast_func=round_float_or_str, last_version=False):
        """
        获取积分
        :param uid:
        :return:
        """
        if last_version:
            score = self.fredis.zscore(self._last_version_key, uid) or 0
        else:
            score = self.fredis.zscore(self._key, uid) or 0
        score = score_cast_func(score)

        return score

    def get_uids_by_rank(self, ranks, withscores=False):
        """
        根据排名获取uid
        :param ranks： [1, 2]
        """
        pipe = self.fredis.pipeline()
        for rank in ranks:
            pipe.zrange(self._key, rank - 1, rank - 1, withscores=withscores)
        return pipe.execute()

    def rank_backup(self, version=None):
        """
        备份当前排名
        :return:
        """
        key_by_date = '%s_%s' % (self._key, version or time.strftime('%F'))
        self.fredis.zunionstore(self._last_version_key, {self._key: 1})
        self.fredis.zunionstore(key_by_date, {self._key: 1})
        self.fredis.expire(key_by_date, 7 * 24 * 3600)

    def init_backup_rank(self):
        if not self.fredis.exists(self._last_version_key):
            self.rank_backup()


class FlowerRank(AllRank):
    """
    鲜花值排行榜
    """


class BiographyRank(AllRank):
    """
    传记排行榜
    """

    def __init__(self, uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = settings.get_father_server(server)
        self._key = self.make_key(uid, server_name=father_server)
        self.fredis = self.get_father_redis(father_server)


class GuildLevelRank(AllRank):
    """
    公会等级排行榜
    """

    def update_level(self, gid, level, exp):
        """ 更新排行

        :param gid: 公会id
        :param level: 等级
        :param exp: 经验
        :return:
        """
        self.fredis.zadd(self._key, gid, generate_rank_score(level * 10000000 + exp))


class WorldBossRank(AllRank):
    """
    世界BOSS伤害排行榜
    """

    def __init__(self, uid='', server='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = settings.get_father_server(server)
        version = kwargs['version']
        self.version = version
        key = '%s||%s||%s' % (self.__class__.__name__, uid, version)
        self._key = self.make_key(key, server_name=father_server)
        self.fredis = self.get_father_redis(father_server)
        self._all_guild_key = "%s_%s" % (self._key, 'all_guild')
        self._inner_guild_key = "%s_%s" % (self._key, 'inner')

    def get_key(self):
        return self._key

    def incr_guild_rank(self, user, score):
        guild_id = user.guild_id
        if user.guild_id:
            self.incr_all_guild_rank(guild_id, score)
            self.incr_inner_guild_rank(guild_id, user.uid, score)

    def incr_all_guild_rank(self, guild_id, score):
        self.fredis.zincrby(self._all_guild_key, guild_id, int(score))
        self.fredis.expire(self._all_guild_key, 7 * 24 * 3600)

    def get_inner_guild_key(self, guild_id):
        return "%s_%s" % (self._inner_guild_key, guild_id)

    def incr_inner_guild_rank(self, guild_id, uid, score):
        key = self.get_inner_guild_key(guild_id)
        self.fredis.zincrby(key, uid, int(score))
        self.fredis.expire(key, 7 * 24 * 3600)

    def get_inner_guild_user(self, guild_id, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        """
        获取公会内排名所有玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        key = self.get_inner_guild_key(guild_id)
        return self.fredis.zrevrange(key, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_all_guild_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        """
        获取公会排名
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrevrange(self._all_guild_key, start, end, withscores=withscores,
                                     score_cast_func=score_cast_func)

    def get_guild_rank(self, guild_id):
        """
        获取公会排名
        :param uid:
        :return:
        """
        rank = self.fredis.zrevrank(self._all_guild_key, guild_id)
        if rank is None:
            rank = -1

        return rank + 1

    def get_guild_score(self, guild_id, score_cast_func=round_float_or_str):
        """
        获取公会积分
        :param uid:
        :return:
        """
        score = self.fredis.zscore(self._all_guild_key, guild_id) or 0
        score = score_cast_func(score)
        return score

    def get_guild_count(self):
        """
        获取公会数
        :return:
        """
        return self.fredis.zcard(self._all_guild_key)

    def guild_rank_backup(self):
        """
        备份当前公会排名
        :return:
        """
        key_by_date = '%s_%s' % (self._all_guild_key, 'backup')
        self.fredis.zunionstore(key_by_date, {self._all_guild_key: 1})
        self.fredis.expire(key_by_date, 7 * 24 * 3600)

    def delete_guild(self):
        """ 删除key

        :return:
        """
        self.fredis.delete(self._all_guild_key)


class BlockRank(AllRank):
    """
    奖励类型 ：剧本类型（1=电影，2=电视，3=综艺，nv=女主角，nan=男主角，audience=用户，medium=媒体,reward=记录获奖人）
    """

    def __init__(self, uid='', server='', date='', *args, **kwargs):
        super(AllRank, self).__init__()
        father_server = settings.get_father_server(server)
        self._key = self.make_key_cls('rank_%s' % uid, server_name=father_server)
        # self.fredis = self.get_father_redis(father_server)
        self.fredis = get_redis_client(settings.public)
        self._key_date = self.key_date(date)

    def key_date(self, date=''):
        from models.block import get_date
        if not date:
            date = get_date()
        return self._key + '||' + date

    # 把玩家添加到所属街区
    def add_user_by_block(self, uid=None, score=0):
        self.fredis.zadd(self._key_date, uid, score)
        self.fredis.expire(self._key_date, 7 * 24 * 3600)

    # 从街区删除玩家（玩家升级街区后操作）
    def delete_user_by_block(self, uid=None):
        self.fredis.zrem(self._key_date, uid)

    # 检查玩家是否在所属街区
    def check_user_exist_by_block(self, uid=None):
        return self.fredis.zscore(self._key_date, uid)

    # 获取编号
    def get_num(self):
        return self.fredis.incr('%s_%s' % (self._key_date, 'num'))

    # 计算玩家所属组
    def get_group(self, uid=None):
        rank = self.fredis.zrank(self._key_date, uid)
        return rank / 100 + 1


    # 记录最大的有人街区
    def set_max_block(self, block_num):
        max_block = int(self.fredis.get(self._key_date)) if self.fredis.get(self._key_date) else 0
        if block_num > max_block:
            self.fredis.set(self._key_date, block_num)

    # 获取最大的有人街区
    def get_max_block(self):
        return int(self.fredis.get(self._key_date)) if self.fredis.get(self._key_date) else 0



    def add_rank(self, uid, rank):
        """
        增加排名
        :param uid:
        :param rank:
        :return:
        """
        self.fredis.zadd(self._key_date, uid, generate_rank_score(rank))
        self.fredis.expire(self._key_date, 7 * 24 * 3600)

    def incr_rank(self, uid, score):
        """
        增加排名
        :param uid:
        :param score:
        :return:
        """
        self.fredis.zincrby(self._key_date, uid, int(score))
        self.fredis.expire(self._key_date, 7 * 24 * 3600)

    def del_rank(self, uid):
        """
        删除排名
        :param uid:
        :return:
        """
        self.fredis.zrem(self._key_date, uid)

    def get_all_user(self, start=0, end=-1, withscores=False, score_cast_func=round_float_or_str):
        """
        获取排名所有玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrevrange(self._key_date, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_rank_user(self, start, end, withscores=False, score_cast_func=round_float_or_str):
        """
        获取指定rank值范围内的玩家
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        return self.fredis.zrangebyscore(self._key_date, start, end, withscores=withscores, score_cast_func=score_cast_func)

    def get_score(self, uid, score_cast_func=round_float_or_str):
        """
        获取积分
        :param uid:
        :return:
        """
        score = self.fredis.zscore(self._key_date, uid) or 0
        score = score_cast_func(score)

        return score

    def get_rank(self, uid):
        """
        获取排名
        :param uid:
        :return:
        """
        rank = self.fredis.zrevrank(self._key_date, uid)
        if rank is None:
            rank = -1

        return rank + 1


ModelManager.register_model_base_tools('level_rank', LevelRank)
# ModelManager.register_model_base_tools('super_active_rank', SuperActiveRank)
# ModelManager.register_model_base_tools('guild_task_rank', GuildTaskRank)
# ModelManager.register_model_base_tools('combat_rank', CombatRank)
# ModelManager.register_model_base_tools('high_ladder_rank', HighladderRank)
# ModelManager.register_model_base_tools('flower_rank', FlowerRank)
# ModelManager.register_model_base_tools('biography_rank', BiographyRank)
# ModelManager.register_model_base_tools('guild_level_rank', GuildLevelRank)
# ModelManager.register_model_base_tools('world_boss_rank', WorldBossRank)
ModelManager.register_model_base_tools('appeal_rank', AppealRank)
ModelManager.register_model_base_tools('output_rank', OutPutRank)
ModelManager.register_model_base_tools('alloutput_rank', AllOutPutRank)
ModelManager.register_model_base_tools('block_rank', BlockRank)
