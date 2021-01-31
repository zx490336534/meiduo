# -*- coding: utf-8 -*-
# @Time    : 2021/1/31 下午2:53
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : urls.py
from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
]
