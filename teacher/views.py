from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.conf import settings    # 获取 settings.py 里边配置的信息

from django.shortcuts import render,redirect
#from django.views.decorators.csrf import csrf_exempt

#from django.conf import settings    # 获取 settings.py 里边配置的信息
import os
from face.models import *
#显示
def all_page(request):
    #读取所有信息
    data = Teacher.objects.all()
    content={'data': data}
    return render(request, 'allt.html', content)


#查sname
def search_teacher(request):
    tname = request.GET['q']
    teacher=Teacher.objects.filter(tname=tname)
    content={'data':teacher}
    return render(request, 'allt.html', content)
# 查sid
def search_teacher_id(request,tid):
    teacher=Teacher.objects.filter(tid=tid)
    content = {'data': teacher}
    print(content)
    return  render(request, 'updatet.html', content)


#改
def update_teacher(request):
    #接受请求参数
    tid = request.POST.get('tid', '')
    tname = request.POST.get('tname', '')
    ttel = request.POST.get('ttel', '')
    cname = request.POST.get('cname', '')
    timg = request.FILES.get('timg', '')
    sid = Clazz.objects.filter(cname=cname)
    # 入库操作
    fname = os.path.join(settings.MEDIA_ROOT, timg.name)

    with open(fname, 'wb') as pic:
        for c in timg.chunks():
            pic.write(c)
    simg = os.path.join(timg.name)
    Teacher.objects.filter(tid=tid).update(sid = sid.first(), tname=tname, ttel=ttel, timg=timg)

    return redirect('/teacher/allPage')

#删除
def delete_teacher(request,tid):
    Teacher.objects.filter(tid=tid).delete()
    return redirect('/teacher/allPage')

#增
# 1.2.前往 add 页
def add_page( request ):
    return render(request, 'addt.html')

# 增
#@csrf_exempt
def add_teacher(request):
    # 接受请求参数
    tname = request.POST.get('tname', '')
    ttel = request.POST.get('ttel', '')
    cname = request.POST.get('cname', '')
    timg = request.FILES.get('timg', '')
    cid=Clazz.objects.filter(cname = cname)
    fname = os.path.join(settings.MEDIA_ROOT, timg.name)
    with open(fname, 'wb') as pic:
        for c in timg.chunks():
            pic.write(c)
    teacher = Teacher()
    teacher.tname = tname
    teacher.ttel = ttel
    teacher.clazz = cid.first()
    # 存访问路径到数据库
    teacher.timg = os.path.join(timg.name)
    teacher.save()

    return redirect('/teacher/allPage')

