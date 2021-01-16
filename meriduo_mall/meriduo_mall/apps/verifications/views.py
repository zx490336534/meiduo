from django.shortcuts import render
from rest_framework.views import APIView


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1. 生成验证码
        # 2. 创建redis连接对象
        # 3. 把验证码存储到redis数据库
        # 4. 利用容联云通讯发送短信验证码
        # 5. 响应
        pass
