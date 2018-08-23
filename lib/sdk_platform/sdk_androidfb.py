# coding: utf-8


def login_verify(req, params=None):
    """登录验证
    Args:
        req: request封装，以下是验证所需参数
            session_id: session_id
        params: 测试专用
    Returns:
        平台相关信息(openid必须有)
    """
    if not params:
        params = {
            'session_id': req.get_argument('session_id'),
            'user_id': req.get_argument('user_id', ''),
        }

    return {
        'openid': params['user_id'],                # 平台用户ID
        'session_id': params['session_id'],         # session_id
    }


if __name__ == '__main__':
    params = {'session_id': 'L1ZNrpw1y3GRv40BWn3iNEFAYZm3mRM7'}
    print login_verify('', params)
