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
    data = Parent.objects.all()
    content={'data': data}
    return render(request, 'allp.html', content)


#查sname
def search_parent(request):
    pname = request.GET['q']
    parent=Parent.objects.filter(pname=pname)
    content={'data':parent}
    return render(request, 'allp.html', content)
# 查sid
def search_parent_id(request,pid):
    parent=Parent.objects.filter(pid=pid)
    content = {'data': parent}
    print(content)
    return  render(request, 'updatep.html', content)


#改
def update_parent(request):
    #接受请求参数
    pid = request.POST.get('pid', '')
    pname = request.POST.get('pname', '')
    ptel = request.POST.get('ptel', '')
    sname = request.POST.get('sname', '')
    pimg = request.FILES.get('pimg', '')
    sid = Student.objects.filter(sname=sname)
    # 入库操作
    fname = os.path.join(settings.MEDIA_ROOT, pimg.name)

    with open(fname, 'wb') as pic:
        for c in pimg.chunks():
            pic.write(c)
    simg = os.path.join(pimg.name)
    Parent.objects.filter(pid=pid).update(sid = sid.first(), pname=pname, ptel=ptel, pimg=pimg)

    return redirect('/parent/allPage')

#删除
def delete_parent(request,pid):
    Parent.objects.filter(pid=pid).delete()
    return redirect('/parent/allPage')

#增
# 1.2.前往 add 页
def add_page( request ):
    return render(request, 'addp.html')

# 增
#@csrf_exempt
def add_parent(request):
    # 接受请求参数
    pname = request.POST.get('pname', '')
    ptel = request.POST.get('ptel', '')
    sname = request.POST.get('sname', '')
    pimg = request.FILES.get('pimg', '')
    sid=Student.objects.filter(sname = sname)
    fname = os.path.join(settings.MEDIA_ROOT, pimg.name)
    with open(fname, 'wb') as pic:
        for c in pimg.chunks():
            pic.write(c)
    parent = Parent()
    parent.pname = pname
    parent.ptel = ptel
    parent.sname = sname
    parent.sid = sid.first()
    # 存访问路径到数据库
    parent.pimg = os.path.join(pimg.name)
    parent.save()

    return redirect('/parent/allPage')

