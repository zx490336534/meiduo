from rest_framework.generics import CreateAPIView


class UserView(CreateAPIView):
    """
    用户注册
    """
    # 指定序列化器
    serializer_class = CreateUserSerializer
