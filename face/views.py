import base64
import sys
import time
import socket
import cv2
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings    # 获取 settings.py 里边配置的信息
from django.shortcuts import render,redirect
#from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings    # 获取 settings.py 里边配置的信息
import os
from . models import *
#显示
def all_page(request):
    #读取所有信息
    data = Student.objects.all()
    content={'data': data}
    return render(request, 'all.html', content)


#查sname
def search_student(request):
    sname = request.GET['q']
    student=Student.objects.filter(sname=sname)
    content={'data':student}
    return render(request, 'all.html', content)
# 查sid
def search_student_id(request,sid):
    student=Student.objects.filter(sid=sid)
    content = {'data': student}
    print(content)
    return  render(request, 'update.html', content)


#改
def update_student(request):
    #接受请求参数
    sid = request.POST.get('sid', '')
    cname = request.POST.get('cname', '')
    sname = request.POST.get('sname', '')
    simg = request.FILES.get('simg', '')
    cid = Clazz.objects.filter(cname=cname)
    # 入库操作
    fname = os.path.join(settings.MEDIA_ROOT, simg.name)

    with open(fname, 'wb') as pic:
        for c in simg.chunks():
            pic.write(c)
    simg = os.path.join(simg.name)

    Student.objects.filter(sid=sid).update(cid = cid.first(), sname=sname, simg=simg)

    return redirect('/face/allPage')

#删除
def delete_student(request,sid):
    Student.objects.filter(sid=sid).delete()
    return redirect('/face/allPage')

#增
# 1.2.前往 add 页
def add_page( request ):
    return render(request, 'add.html')

# 增
#@csrf_exempt
def add_student(request):
    # 接受请求参数
    cname = request.POST.get('cname', '')
    sname = request.POST.get('sname', '')
    simg = request.FILES.get('simg', '')
    cid=Clazz.objects.filter(cname = cname)
    fname = os.path.join(settings.MEDIA_ROOT, simg.name)
    with open(fname, 'wb') as pic:
        for c in simg.chunks():
            pic.write(c)
    student = Student()
    student.sname = sname
    student.cid = cid.first()
    # 存访问路径到数据库
    student.simg = os.path.join(simg.name)
    student.save()

    return redirect('/face/allPage')


def face_page(request):#上传文件页面
    return render(request, 'facenet.html')

def face_page2(request):
    return render(request, 'facecamera.html')

#打开摄像头
#imge_path = os.path.dirname(os.path.abspath(__file__))+'\\img.jpg'
#settings.MEDIA_ROOT
imge_path = os.path.join(settings.MEDIA_ROOT, 'img.jpg')
#avi_path=os.path.dirname(os.path.abspath(__file__))+'\\output.avi'
avi_path = os.path.join(settings.MEDIA_ROOT, 'output.avi')

def imgeTobase64():
	with open(imge_path,'rb') as f:
		base64_data = base64.b64encode(f.read())
	s = base64_data.decode()
	#print("data:imge/jpeg;base64,%s"%s)
	s = s[s.find(',')+1:]
	#print s
	return s


def camer_open():
    cap = cv2.VideoCapture(0)
    return cap


def camer_close(fun_cap):
    fun_cap.release()
    cv2.destroyAllWindows()



fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(avi_path, fourcc, 20.0, (640, 480))


def make_photo(capp):
    while True:

        ret_cap, frame = capp.read()
        time.sleep(0.2)
        if ret_cap:
            print("read ok")
            color = (0, 0, 0)
            img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)#COLOR_RGB2GRAY
            cv2.imwrite(imge_path, img_gray)
            image_base64 = imgeTobase64()

            # draw_0 = cv2.rectangle(image, (2*w, 2*h), (3*w, 3*h), (255, 0, 0), 2)

            # frame = cv2.flip(frame,0)
            # write the flipped frame
            out.write(frame)
            cv2.imshow("capture", frame)  # ������
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camer_close(capp)
                break
        else:
            break
#识别模块
def socket_client(filepath):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('221.205.237.173', 6666))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print(s.recv(1024).decode("utf-8"))

    if os.path.isfile(filepath):

        fhead = filepath + ' ' + str(os.stat(filepath).st_size)
        print('client filepath: {0}'.format(filepath))
        s.send(bytes(fhead, encoding='utf-8'))
        print(s.recv(1024).decode("utf-8"))

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            s.send(data)

    print(s.recv(1024).decode("utf-8"))
    res = s.recv(1024).decode("utf-8")
    s.close()
    return res


def face_search(res):
    obj = Student.objects.filter(sname=res)
    type='s'
    if (obj.exists()==False):
        obj = Parent.objects.filter(pname=res)
        type='p'
        if (obj.exists()==False):
            obj = Teacher.objects.filter(tname=res)
            type='t'
    return obj,type



def face_net(request):#识别该人是否已在数据库中
    #接受请求参数
    simg = request.FILES.get('simg', None)

    #文件未上传
    if simg == None:
        return HttpResponse('未添加文件')

    #文件上传
    fname = os.path.join('static/media/', simg.name)
    with open(fname, 'wb') as pic:
        for c in simg.chunks():
            pic.write(c)
    #判断是否是本校的学生或者是否是本校学生的家长，响应显示找到的学生的信息。
    #sid存放找到的学生id
    # 匹配成功时
    #student = Student()
    res = socket_client(fname)
    obj,type=face_search(res)

    if obj.exists()==False:
        return render(request, 'fail.html')
    elif type=='s':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'all.html', content)
    elif type=='p':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'allp.html', content)
    elif type=='t':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'allt.html', content)
    #匹配失败时
    else:
        #响应页面还没加
        return HttpResponse('识别类型失败')



def face_camera(request):
    cap = camer_open()
    make_photo(cap)
    res = socket_client('static/media/img.jpg')
    obj,type=face_search(res)

    if obj.exists()==False:
        return render(request, 'failcamera.html')
    elif type=='s':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'all.html', content)
    elif type=='p':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'allp.html', content)
    elif type=='t':
        content = {'data': obj}
        # 响应显示找到的学生的信息
        return render(request, 'allt.html', content)
    #匹配失败时
    else:
        #响应页面还没加
        return HttpResponse('识别类型失败')