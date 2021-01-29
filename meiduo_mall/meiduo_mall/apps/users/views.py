from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUserSerializer
from .models import User


class UserView(CreateAPIView):
    """
    用户注册
    """
    # 指定序列化器
    serializer_class = CreateUserSerializer


class UserCountView(APIView):
    """判断用户是否已注册"""

    def get(self, request, username):
        # 查询user表
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobileCountView(APIView):
    """判断手机号是否已注册"""

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)
