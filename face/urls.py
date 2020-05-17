#-*-coding = utf-8 -*-
#@Time:2020/5/15 22:27
#@Author:糊糊
#@File:urls.py
#@Software:PyCharm

from django.conf.urls import url
from . import views
app_name='face'
urlpatterns = [
    url(r'^allPage/', views.all_page,name='all_page'),
    url(r'^addPage/$', views.add_page,name='add_page'),  # 前往新增学生的网页
    url(r'^addStudent/$', views.add_student),  # 添加学生
    url(r'^search/$', views.search_student),  # 根据 sname查找学生的 dao 操作
    url(r'^get/(?P<sid>[0-9]*)/$', views.search_student_id),  # 根据 pid 查找学生
    url(r'^updateStudent/$', views.update_student),  # 修改学生
    url(r'^delete/(?P<sid>[0-9]*)/$', views.delete_student,name='delete'),  # 删除学生

    url(r'^facepage/$', views.face_page,name='face_page'),
    url(r'^facepage2/$', views.face_page2,name='face_page2'),
    url(r'^facenet/$', views.face_net,name='face_net'),
    url(r'^facecamera/$', views.face_camera,name='face_camera'),

]