#!/usr/bin/python
# encoding: utf-8

'''
获得mixi牧场的所有配置信息，存入mxfarm_config.py中，mxfarm_config可以直接被引用
mxfarm_config:
    config = {
    }
'''

def get_all_config(back_config=True):
    import os, sys
    import cPickle as pickle


    cur_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir + os.sep
    #sys.path.insert(0, os.path.join(cur_dir, ".."))
    sys.path.append(os.path.join(cur_dir))
    
    try:
        import settings
        from models.config import Config, FrontConfig
    except:
        import settings
        settings.set_env('yyf')
        from models.config import Config, FrontConfig

    config_dict = {}
    if back_config:
        for config_key in settings.BACK_CONFIG_NAME_LIST:
            _c = Config.get(config_key)
            if _c.version:
                config_dict[config_key] = _c.value
        file_name = cur_dir + '/test/local_config_back.py'
    else:
        for config_key in settings.FRONT_CONFIG_NAME_LIST:
            _c = FrontConfig.get(config_key)
            if _c.version:
                config_dict[config_key] = _c.value
        file_name = cur_dir + '/test/local_config_front.py'

    f = open(file_name, 'w')
    # d = str(config_dict)
    #
    # f.write('config='+d)
    pickle.dump(config_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()
    return file_name

if __name__ == '__main__':
    get_all_config()
