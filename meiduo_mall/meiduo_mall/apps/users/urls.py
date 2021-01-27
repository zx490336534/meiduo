# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 下午7:37
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册用户
    url(r'^users/$', views.UserView.as_view()),
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UserView.as_view())
]
