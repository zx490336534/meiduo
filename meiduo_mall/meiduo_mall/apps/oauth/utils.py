# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 下午3:31
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : utils.py
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData


def generate_save_user_token(openid):
    """
    使用itsdangerous对原始的openid进行签名
    :param openid: 原始的openid
    :return: 签名后的openid
    """
    # 创建序列化器对象，指定秘钥和过期时间（10分钟）
    serializer = TJSSerializer(settings.SECRET_KEY, 600)
    # 准备原始的openid
    data = {'openid': openid}
    # 对openid进行签名,返回签名之后的bytes类型的字符串
    token = serializer.dumps(data)
    # 将bytes类型的字符串转成标准的字符串，并返回
    return token.decode()


def check_save_user_token(access_token):
    """
    将access_token还原为openid
    :param access_token: 签名后的openid
    :return: 原始的openid
    """
    # 创建序列化器对象，指定秘钥和过期时间（10分钟）
    serializer = TJSSerializer(settings.SECRET_KEY, 600)

    try:
        data = serializer.loads(access_token)
    except BadData:
        return None
    else:
        openid = data.get('openid')
        return openid
