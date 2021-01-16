# -*- coding: utf-8 -*-
# @Time    : 2021/1/16 下午9:52
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    # 发短信
    url(r'^smscode/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view())
]
