# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 上午9:05
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : utils.py

def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数，多追加user_id和username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
