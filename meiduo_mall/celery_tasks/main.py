# -*- coding: utf-8 -*-
# @Time    : 2021/1/18 下午9:59
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : main.py
# celery启动文件

from celery import Celery

# 创建celery实例
celery_app = Celery('meiduo')

# 加载celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
