# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 下午7:38
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : serializers.py
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""

    # 序列化器的所有字段: ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 序列化器需要校验的所有字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 模型中已存在的字段 ['username', 'password', 'mobile']
    # 需要序列化的字段 ['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段 ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']

    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User  # 从User模型中映射序列化器字段
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'token']
        extra_kwargs = {  # 修改字段选项
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """校验手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):  # 联合校验
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        # 向redis存储数据时都是以字符串进行存储的，取出来后都是bytes类型
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除数据库模型类中不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 把密码加密后再赋值给user的password属性
        user.save()
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 引用jwt中的jwt_payload_handler函数(生成payload)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 函数引用 生成jwt
        payload = jwt_payload_handler(user)  # 根据user生成用户相关的载荷
        token = jwt_encode_handler(payload) # 传入载荷生成完整的jwt
        user.token = token
        return user
