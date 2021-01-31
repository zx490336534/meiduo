import logging

from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.models import OAuthQQUser

logger = logging.getLogger('django')


class QQAuthURLView(APIView):

    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.query_params.get('next')
        if not next:
            next = '/'

        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        login_url = oauth.get_qq_url()

        return Response({'login_url': login_url})


class QQAuthUserView(APIView):
    """
        用户扫码登录的回调处理
        OAuth2.0认证:处理扫码回调操作
    """

    def get(self, request):
        # 提取code请求参数
        # 使用code向QQ服务器请求access_token
        # 使用access_token向QQ服务器请求openid
        # 使用openid查询该QQ用户是否在美多商城中绑定过用户
        # 如果openid没绑定美多商城用户，创建用户并绑定到openid
        # 如果openid已绑定美多商城用户，直接生成JWT token，并返回

        # 提取code请求参数
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建OAuthQQ对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.info(e)
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # 使用openid查询该QQ用户是否在美多商城中绑定过用户
        try:
            oauthqquser_model = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没绑定美多商城用户，创建用户并绑定到openid
            pass
        else:
            # 如果openid已绑定美多商城用户，直接生成JWT token，并返回
            pass
