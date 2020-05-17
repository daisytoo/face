#-*-coding = utf-8 -*-
#@Time:2020/5/16 7:36
#@Author:糊糊
#@File:urls.py
#@Software:PyCharm

from django.conf.urls import url
from . import views
app_name='parent'
urlpatterns = [
    url(r'^allPage/', views.all_page, name='all_page'),
    url(r'^addPage/$', views.add_page, name='add_page'),  # 前往新增家长的网页
    url(r'^addParent/$', views.add_parent),  # 添加家长
    url(r'^search/$', views.search_parent),  # 根据 pname 查找
    url(r'^get/(?P<pid>[0-9]*)/$', views.search_parent_id),  # 根据 pid 查找
    url(r'^updateParent/$', views.update_parent),  # 修改
    url(r'^delete/(?P<pid>[0-9]*)/$', views.delete_parent, name='delete'),  # 删除家长

]


