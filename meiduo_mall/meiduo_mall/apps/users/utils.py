# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 上午9:05
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : utils.py
import re

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登录视图的构造响应数据函数，多追加user_id和username"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def get_user_by_account(account):
    """根据传入的账号获取用户信息"""
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """修改用户认证系统的后端，支持多账号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据传入的username获取user对象。username可以是手机号也可以是账号
        user = get_user_by_account(username)

        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user
