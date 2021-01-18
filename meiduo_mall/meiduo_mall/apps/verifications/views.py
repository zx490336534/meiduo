import random
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from . import constants
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
        # 3.如果获取到类标记，说明手机号频繁发送短信
        if send_flag:
            return Response({"message": "发送短信过于频繁"}, status=status.HTTP_400_BAD_REQUEST)
        # 4. 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.debug(sms_code)

        # 创建redis管道 把多次redis操作装入管道中，将来一次性去执行，减少redis连接操作
        pl = redis_conn.pipeline()
        # 5. 把验证码存储到redis数据库
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 6. 把验证码存储到redis数据库
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行管道
        pl.execute()

        # 7. 利用容联云通讯发送短信验证码
        # CCP().send_template_sms(self, 手机号, [验证码，5], 1):
        CCP().send_template_sms(mobile, [sms_code,
                                         constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # 8. 响应
        return Response({'message': 'ok'})
