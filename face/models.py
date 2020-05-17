from django.db import models

# Create your models here.
class Face(models.Model):
    #本次匹配的id，自动递增
    fid = models.AutoField(primary_key=True)
    #本次匹配的时间
    create = models.DateTimeField(auto_now_add=True)
    #匹配到的id
    mid = models.IntegerField(default=-1)
    #匹配到的名字
    mname = models.CharField(max_length=30,default='no matching')
    #匹配到的照片
    fimg=models.ImageField(upload_to='upload',max_length=200)

#    class Meta:
#        db_table = 't_face'
    def __str__(self):
        return u'Face:%d%d'%(self.fid,self.mid)

#班级主表
class Clazz(models.Model):
    cid = models.AutoField(primary_key=True)
    # 班级编号
    cname = models.CharField(max_length=30, default='一年级一班')
    def __str__(self):
        return u'Clazz:%d%s'%(self.cid,self.cname)
#老师
class Teacher(models.Model):
    # 编号
    tid = models.AutoField(primary_key=True)
    # 管理班级编号
    clazz = models.OneToOneField(Clazz,on_delete=models.CASCADE)
    # 班级名
    tname = models.CharField(max_length=30, default='李小明')
    # 电话
    ttel = models.CharField(max_length=11)
    # 照片
    timg = models.ImageField(upload_to='', max_length=200)

    def __str__(self):
        return u'Teacher:%d%s%d'%(self.tid,self.tname,self.clazz.cid)

#学生
class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    # 班级编号
    cid = models.ForeignKey(Clazz,on_delete=models.CASCADE)#IntegerField(primary_key=True)
    sname = models.CharField(max_length=30, default='李小明')
    # 照片
    simg = models.ImageField(upload_to='', max_length=200)

    def __str__(self):
        return u'Student:%d%s'%(self.sid,self.sname)
#家长
class Parent(models.Model):
    pid = models.AutoField(primary_key=True)
    # 班级编号
    pname = models.CharField(max_length=30, default='李明')
    # 电话
    ptel = models.CharField(max_length=11)
    # 照片
    pimg = models.ImageField(upload_to='', max_length=200)
    # 学生
    sid = models.ForeignKey(Student,on_delete=models.CASCADE)
    def __str__(self):
        return u'Parent:%d%s'%(self.pid,self.pname)



#给一个学生添加家长 多对多添加
def insertData_p(sid,*parentids):
    try:
        s = Student.objects.get(sid=sid)
        parentList = []
        for pi in parentids:
            try:
                p = Parent.objects.get(pid=pi)
                parentList.append(p)
                s.stu.add(*parentList)
            except Parent.DoesNotExit:
                print('不存在这位家长%d' % pi)
                # p = Parent.objects.create(pid = pi)
            parentList.append(p)
    except Student.DoesNotExist:
        print('不存在这名学生%d'%sid)
        #s = Student.objects.create(sid=sid,cid=cid,sname=sname,simg=simg)


#给一个班添加学生
def insertData_s(cid,clsname,*sids):
    try:
        cls=Clazz.objects.get(cid=cid)
        for si in sids:
            try:
                s = Student.objects.get(sid=si)
                s.cid=cls.cid
            except Parent.DoesNotExit:
                print('不存在这名学生%d' % si)
    except Clazz.DoesNotExit:
        print('不存在这个班%d' % cid)

# #根据班级名称获取班级对象
# def getClass(cname):
#     try:
#         cls = Clazz.objects.get(cname=cname)
#     except Clazz.DoesNotExist:
#         cls = Clazz.objects.create(cname=cname)
#     return cls
#
# #获取学生对象列表
# def getStudentList(*studentnames):
#     studentList = []
#
#     for sn in studentnames:
#         try:
#             c = Student.objects.get(sname=sn)
#         except Student.DoesNotExist:
#             print('班级不存在')
#             #c = Student.objects.create(sname=sn)
#         studentList.append(c)
#
#     return studentList
#
# def registerStu(sname,cname,*coursenames):
#     #1.获取班级对象
#     cls = getClass(cname)
#     #2.获取课程对象列表
#     courseList = getCourseList(*coursenames)
#     #3.插入学生表数据
#     try:
#         stu = Student.objects.get(sname=sname)
#     except Student.DoesNotExist:
#         stu = Student.objects.create(sname=sname,cls=cls)
#     #4.插入中间表数据
#     stu.cour.add(*courseList)
#
#     return True