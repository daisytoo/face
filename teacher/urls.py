#-*-coding = utf-8 -*-
#@Time:2020/5/16 23:47
#@Author:糊糊
#@File:urls.py
#@Software:PyCharm
from django.conf.urls import url
from . import views
app_name='teacher'
urlpatterns = [
    url(r'^allPage/', views.all_page, name='all_page'),
    url(r'^addPage/$', views.add_page, name='add_page'),  # 前往新增老师的网页
    url(r'^addTeacher/$', views.add_teacher),  # 添加老师
    url(r'^search/$', views.search_teacher),  # 根据 tname 查找
    url(r'^get/(?P<pid>[0-9]*)/$', views.search_teacher_id),  # 根据 tid 查找
    url(r'^updateTeacher/$', views.update_teacher),  # 修改
    url(r'^delete/(?P<pid>[0-9]*)/$', views.delete_teacher, name='delete'),  # 删除老师
]