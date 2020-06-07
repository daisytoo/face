1、本系统使用python语言+django框架，实现中小学校园人脸识别安防应用。前端主要使用了layui框架，使用简单，美观大方。
2、系统模块介绍
2.1App
Django中App可以让我们将不同类型的功能分成多个不同的App应用来开发。本系统一共有三个app，其中face主要实现学生信息的增删改查、人脸识别模块和目标定位模块的视频展示；parent和teacher主要实现家长和教师的信息的增删改查。
2.2url
把本该在项目目录下的urls.py中进行路由匹配的功能给分发到各个不同的App内，在其中新建urls.py文件来进行路由匹配;在项目目录下的urls.py中建立分发指引路径。本系统的主路由有admin,face,teacher,parent，分别对应app和django自带管理后台的功能。在设置子路由时，在views页面和html页面通过path使用name参数为其命名反向获取URL使用路由。
2.3Views
Views接收并处理请求，调用模型和模版，响应请求，主要的功能在每个app的views中实现。
2.3.1管理员部分
管理员实现基本的登录登出管理信息的功能。登录功能我们采用基于 token 的鉴权机制。
2.3.2人物部分  
user函数即管理员部分实现对学生、老师和家长的信息查询和管理。每个app的views中有关数据的添加和更新的提交表单部分涉及到 csrf 跨站请求伪造的问题。
我们给表单 form加了 token，django 在渲染模板 时会把 {% csrf_token %} 替换成<input type="hidden", name='csrfmiddlewaretoken' value=服务器随机生成的 token>元素。在提交表单时启动 'django.middleware.csrf.CsrfViewMiddleware' 中间件验证 csrf_token 的，防止恶意请求。
2.3.3人脸识别部分  
face的views中有专门的识别函数，通过socket连接识别模块实现对上传并存储到服务器的图像文件进行身份识别并和已有数据中的人脸进行匹配。
摄像头的调用采用 openCV 模块。在views中调用openCV相关函数来获取视频，按帧读取视频，保存到 MEDIA_URL 路径中，当根据操作者操作停止录像，自动保存当前图像到 相同路径，调用人脸识别模块实现识别功能。
2.3.4目标定位部分
主要通过在网页中嵌入视频的方式实现对目标定位部分的展示，基于设备限制在代码中没有具体实现原理。
2.4models
在setting中的DATABASES进行mysql的配置
用class的方式建表，再将model层转为迁移文件migration，之后将新版本的迁移文件执行，更新数据库。
结合Navicat使用，可以更方便地查看数据库信息。
2.5templates
Django中的模版文件是html代码+逻辑控制代码组成，这里的html模板是一个文本，用于分离文档的表现形式和内容。所有模版文件即html都必须放在templates目录下。
2.6静态文件
程序目录添加一个static文件夹，把静态文件放到这个文件夹下。其中有layui框架的css、图片等文件和数据库人脸照片存储以及用于测试人脸识别的部分图片。

