import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
import logging

from meiduo_mall.libs.yuntongxun.sms import CCP

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1. 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 2. 从redits中获取发送标记
        # 60秒内不允许重发发送短信
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({"message": "发送短信过于频繁"}, status=status.HTTP_400_BAD_REQUEST)
        # 3. 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.debug(sms_code)
        # 4. 把验证码存储到redis数据库
        redis_conn.setex('sms_%s' % mobile, 300, sms_code)
        # 5. 利用容联云通讯发送短信验证码
        # CCP().send_template_sms(self, 手机号, [验证码，5], 1):
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 6. 响应
        return Response({'message': 'ok'})
