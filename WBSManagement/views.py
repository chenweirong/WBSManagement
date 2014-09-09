#-*- encoding:UTF-8 -*- 
from django.shortcuts import HttpResponse,render_to_response
from django.http import HttpResponseBadRequest,HttpResponseRedirect
from awooautils import create_verifycode,geticonlist
from django.contrib.auth.decorators import login_required
from WBSManagement.models import *
from WBSManagement import threadlocals
from django.contrib.auth.models import User
import StringIO


def validate(request):
    mstream=StringIO.StringIO()
    validate_code=create_verifycode(size=(120,24),draw_lines=False,draw_points=False)
    
    img=validate_code[0]
    img.save(mstream,"GIF")
    request.session['validate']=validate_code[1]
    
    return HttpResponse(mstream.getvalue(),"image/gif")

def loginhtml(request):
    return render_to_response('login.html')

from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
#用于提高网站安全性
@csrf_exempt

def userlogin(request):
    print request
    if request.method != 'POST':
        return HttpResponseBadRequest("错：Need Post Method. 调用方法不正确.")
        #result={"message":"Need Post Method. 调用方法不正确.","error":400,}
        #return HttpResponse(simplejson.dumps(result,ensure_ascii=False))
    if 'username' not in request.POST or 'password' not in request.POST or 'verifyCode' not in request.POST:
        return HttpResponseBadRequest("错：POST参数错误")
    if request.POST['verifyCode'].upper()!=request.session['validate'].upper():
        return HttpResponseBadRequest("错：验证码错误")

    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            #redictory
            return HttpResponse("登录成功")
        else:
            return HttpResponseBadRequest("错：用户账户不可用")
    else:
        return HttpResponseBadRequest("错：用户账户不可用")

def userlogout(request):
    logout(request)
    request.session.clear()
    return HttpResponseRedirect('/')

@login_required
#@login_required表示只有用户在登录的情况下才能调用该视图，否则将自动重定向至登录页面。
def workplace(request):
    loginusername=u'%s%s'%(request.user.last_name,request.user.first_name)
    return render_to_response('mainbase.html',{'loginusername':loginusername})


def chkenv(request):
    rs=geticonlist()
    return HttpResponse(rs)

"""
此函数为获取当前执行操作用户，并在保存时存入数据库。
"""
def GetUserName():
    #获取当前登录用户ID，并转换成字符串格式。
    publisherID = str(threadlocals.get_current_user()) 
    #通过用户名查询Django自己创建的User数据库中的用户，获取用户的姓名。
    #要查询Django的User的modle需要引入from django.contrib.auth.models import User
    return User.objects.get(username=publisherID).last_name + User.objects.get(username=publisherID).first_name