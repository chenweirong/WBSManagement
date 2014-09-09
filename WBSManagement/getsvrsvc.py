#-*- encoding:UTF-8 -*- 

from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils import simplejson as json
from WBSManagement.models import *
from WBSManagement import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import models

from awooautils import getServerTime,checkStudentPwd,respJson

"""
如果 objects.get得到的结果，就需要用 awooaJSONEncoder进行编码
如果 objects.filter得到的结果，直接使用 ValuesQuerySetToDict 即可
filter 不支持 DoexNotExist 需要用 exists()
"""
class awooaJSONEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, models.query.QuerySet):
            return json.loads(serializers.serialize('json',obj))
        if isinstance(obj, models.Model):
            return json.loads(serializers.serialize('json',[obj])[1:-1])
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]
    #return serializers.serialize("json", vqs)

@login_required
@csrf_exempt
def getmenu(request):
    print request.META['REMOTE_ADDR']#显示客户端IP
    rtn_menu={}
    menus_from_db=FirstLevelMenu.objects.values('menuid','icon','menuname')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    for item in data_dict:
        submenu_from_db=SecondLevelMenu.objects.filter(firstlevelmenuid=item['menuid']).values('menuid','icon','menuname','url')
        sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
        item['menus']=sub_data_dict
    rtn_menu['menus']=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#新加测试单元
#------------------------------------------------------------------------------#

#学生信息
def getStudentInfo(request):
    
    rtn_menu={}
    menus_from_db=StudentInfo.objects.values('sid','nickname','sex','email','telnumber1','telnumber2','qqnumber','mmnumber','companyname','positionname','photo','startlevelid')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    for item in data_dict:
        submenu_from_db=Classname.objects.filter(classname=item['startlevelid']).values('classname')
        sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
        tmpvariable=sub_data_dict[0].values()
        item['startlevelid']=tmpvariable[0]
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#课程配置
def gettestmenu(request):
    rtn_menu={}
    #menus_from_db=Classlesson.objects.values('clclassname','clcoursewarename')
    menus_from_db=Classlesson.objects.filter(clclassname='2008级1班').values('clclassname','clcoursewarename')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    '''
    for item in data_dict:
        submenu_from_db=Classlesson.objects.filter(clclassname=item['clclassname']).values('clclassname','clcoursewarename')
        sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
        tmpvariable=sub_data_dict[0].values()
        item['clclassname']=tmpvariable[0]
    '''
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))
    
#成绩
def getScore(request):
    rtn_menu={}
    menus_from_db=Score.objects.values('sid','studentname','levelid','classlessontype','usuallyAbsences','usuallyLate','usuallyLeaveEarly','excamscore','totalScore','dscpt')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#发布提醒
def getAlarm(request):
    rtn_menu={}
    menus_from_db=Alarm.objects.values('classname','studentid','publisher','title','dscpt','repeatimes','interval')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    for item in data_dict:
        submenu_from_db=Classname.objects.filter(id=item['classname']).values('classname')
        sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
        tmpvariable=sub_data_dict[0].values()
        item['classname']=tmpvariable[0]
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#班级活动
def getClassActivities(request):
    rtn_menu={}
    menus_from_db=ClassActivities.objects.values('classname','publisher','photo','title','dscpt','appointurl')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    for item in data_dict:
        submenu_from_db=Classname.objects.filter(classname=item['classname']).values('classname')
        sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
        tmpvariable=sub_data_dict[0].values()
        item['classname']=tmpvariable[0]
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#班级编组
def getClassgroup(request):
    rtn_menu={}
    menus_from_db=Classgroup.objects.values('gid','classname')
    data_dict=ValuesQuerySetToDict(menus_from_db)
    rtn_menu=data_dict
    return respJson(HttpResponse(json.dumps(rtn_menu,ensure_ascii=False)))

#------------------------------------------------------------------------------#
# from django.contrib.auth.models import User
@csrf_exempt
@login_required
def updpassword(request):
    newpasswd=request.POST['newpwd']
    try:
        request.user.set_password(newpasswd)
        request.user.save()
    except:
        return HttpResponseBadRequest('set_password,错误')
    return HttpResponse('修改密码成功')

"""
#以Get方式提供给客户端数据通讯、文件下载功能
#基本操作协议： req?type=x&student=xxx&cid=xxxx&....
#type:功能说明
    type=0 或者系统参数设置为系统测试，就只返回固定格式服务器时间
    type=1 学生登录,由于每个指令都要带学生id和密码cid，本指令只是返回学生的最新服务器相关信息
    type=2 学生修改密码
    type=3 取json数据 配合dataid
    type=4 下载文件
    type=5 服务端纪录日志
#student:学生id
#cid:学生密码平房求和算法结果
"""
from django.core.servers.basehttp import FileWrapper
import base64
#流方式读文件并下载，须支持 Http Accepts-Range
def reqentrance(request):
    retrst={}
    retrst['result'] = 0
    
    if 'type' not in request.GET:
        retrst['result'] = -1
        retrst['errmsg'] = 'GET参数错误，缺少type'
        return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))
    
    type=request.GET['type']

    def getCfgParasValue(t_paraname):
        try:
            retrst[t_paraname] = CfgParas.objects.get(paraname=t_paraname).paravalue
        except CfgParas.DoesNotExist:
            retrst[t_paraname] = ''
            pass
        except Exception as e:
            raise e
        
    def checkStudentAndcidExist():
        if 'student' not in request.GET :
            retrst['result'] = -1
            retrst['errmsg'] = '错误,缺少GET参数student'

        if 'cid' not in request.GET :
            retrst['result'] = -1
            retrst['errmsg'] = '错误,缺少GET参数cid'
#             return HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False))
        return request.GET['student'], request.GET['cid']

    def checkStudentAndcid(g_sid, g_cid):
        try:
            student_fromdb =  StudentInfo.objects.filter(sid = g_sid).values()
            #student_fromdb =  StudentInfo.objects.get(sid = request.GET['student'])
#         except StudentInfo.DoesNotExist:
#             retrst['result'] = -1
#             retrst['errmsg'] = '学生ID[%s]不存在'%(request.GET['student'])
#             return HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False))
        except Exception as e:
            raise e
        
        if not student_fromdb.exists():
            retrst['result'] = -1
            retrst['errmsg'] = '学生ID[%s]不存在'%(g_sid)
#            return HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False))
#**********************************************************************************************       
#        if not checkStudentPwd(student_fromdb[0]['sid'], student_fromdb[0]['pwd'], g_cid):
#            retrst['result'] = -1
#            retrst['errmsg'] = '学生密码错误'
#             return HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)) 
#**********************************************************************************************     
        return student_fromdb 

    if type == '0':
        """
        type=0 或者系统参数设置为系统测试，就只返回固定格式服务器时间
        """
        getCfgParasValue('version')  
        getCfgParasValue('mainServerURL')  
        retrst['serverTime'] = getServerTime()
        return respJson(HttpResponse(json.dumps(retrst,  ensure_ascii=False)))
    
    elif type == '1':
        """
        学生登录，返回该学生相应信息
        """
        g_sid, g_cid = checkStudentAndcidExist()
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))       

        student_fromdb = checkStudentAndcid(g_sid,g_cid).values('nickname','photo','email','sid','startlevelid_id')
        
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)) )              

        retrst['result'] = 0
        retrst['content'] = ValuesQuerySetToDict(student_fromdb) 
        retrst['content'][0]['startlevelid_id']=Classname.objects.filter(classname=student_fromdb[0]['startlevelid_id']).values()[0]['classname']
        return respJson(HttpResponse(json.dumps(retrst,  ensure_ascii=False, cls=awooaJSONEncoder)))
    
    elif type == '2':
        """
        type=2 修改密码， 由ipad客户端发命令 newpwd为base64字符串编码
        """
        g_sid, g_cid = checkStudentAndcidExist()
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)) )      
        
        if 'newpwd' not in request.GET:
            retrst['result'] = -1
            retrst['errmsg'] = '错误,缺少GET参数'
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))

        checkStudentAndcid(g_sid, g_cid)
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))       
        
        newpwd=base64.decodestring(request.GET['newpwd'])
        
        student2 = StudentInfo.objects.get(sid=g_sid)
        student2.pwd = newpwd
        try:
            student2.save()
        except Exception as e:
            raise e
        
        retrst['result'] = 0
        retrst['content'] = '新密码已更新，下次登录时启用'
        return respJson(HttpResponse(json.dumps(retrst,  ensure_ascii=False)))

    elif type == '3':
        """
        配合dataid取json 数据
        dataid:
            101 : 级别信息
            102 : 类别
            103 : 子类别
        """
        g_sid, g_cid = checkStudentAndcidExist()
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))       
        
        if 'dataid' not in request.GET:
            retrst['result'] = -1
            retrst['errmsg'] = '错误,缺少GET参数dataid'
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))
        dataid = request.GET['dataid']

        checkStudentAndcid(g_sid, g_cid)
        if retrst['result'] != 0:
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))       

        if dataid == '101' or dataid == "top":
            student=request.GET['student']
            classname = StudentInfo.objects.filter(sid=student).values('startlevelid')
            data_fromdb = Classlesson.objects.filter(clclassname=classname).values('clcoursewarename')
            data_dict=ValuesQuerySetToDict(data_fromdb)
            numberOfLesson = 0
            for item in data_dict:
                item['课程名称'] = item['clcoursewarename']
                start_time = Classlessontype.objects.filter(classlessontype=item['clcoursewarename']).values('startday')
                for item_time in start_time:
                    item['上课时间'] = item_time['startday']
                lesson_number = Classlessontype.objects.filter(classlessontype=item['clcoursewarename']).values('classlessontypenumber')
                for item_number in lesson_number:
                    item['排序编号'] = item_number['classlessontypenumber']
                temp_item_cate = ValuesQuerySetToDict(Lesson.objects.filter(coursewarename=item['clcoursewarename']).values('lesson'))
                delete_repdictkey_long =[]
                delete_repdictkey_short =[]
                """获取此课程包含有那些课程分类（如“课程大纲”，“课程PPT”...）"""
                for repitem in temp_item_cate:
                    for key in repitem:
                        delete_repdictkey_long.append(repitem[key])
                """去除上面所获取的课程分类中的重复项"""
                delete_repdictkey_short = list(set(delete_repdictkey_long))
                delete_repdictkey = []
                for delete_tmp in delete_repdictkey_short:
                    temp_dict_name = {}
                    temp_dict_name['课程分类名'] = delete_tmp
                    type_number = Lessontype.objects.filter(lessontype=delete_tmp).values('lessontypenumber')
                    for item_number in type_number:
                        temp_dict_name['排序编号'] = item_number['lessontypenumber']
                    lesson_book = ValuesQuerySetToDict(Lesson.objects.filter(coursewarename=item['clcoursewarename'],lesson=delete_tmp).values())
                    
                    for tmp_lesson_book in lesson_book:
                            tmp_lesson_book['文件size']=tmp_lesson_book['filesize']
                            del tmp_lesson_book['filesize']
                            tmp_lesson_book['文件']=tmp_lesson_book['filerealname']
                            del tmp_lesson_book['filerealname']
                            tmp_lesson_book['排序编号']=tmp_lesson_book['lessonnumber']
                            del tmp_lesson_book['lessonnumber']

                    temp_dict_name['资料'] = lesson_book
                    delete_repdictkey.append(temp_dict_name)
                item['课程资料'] = delete_repdictkey
                del item['clcoursewarename']
                numberOfLesson+=1
            retrst['count'] = numberOfLesson
            retrst['servertime'] = getServerTime()

        elif dataid == '102' or dataid == "leftNav":
            student=request.GET['student']
            data_fromdb = Score.objects.filter(sid=student).values('classlessontype','usuallyAbsences','usuallyLate',
                                                                   'usuallyLeaveEarly','excamscore','totalScore','dscpt')
            number_score = 0
            for item in data_fromdb:
                item['课程名称']=item['classlessontype']
                del item['classlessontype']
                item['迟到次数']=item['usuallyLate']
                del item['usuallyLate']
                item['考试成绩']=item['excamscore']
                del item['excamscore']
                item['备注']=item['dscpt']
                del item['dscpt']
                item['早退次数']=item['usuallyLeaveEarly']
                del item['usuallyLeaveEarly']
                item['总成绩']=item['totalScore']
                del item['totalScore']
                item['缺课节数']=item['usuallyAbsences']
                del item['usuallyAbsences']
                number_score+=1
            retrst['count'] = number_score
            retrst['servertime'] = getServerTime()
            
        elif dataid == '103' or dataid == "panel":
            student=request.GET['student']
            classname = StudentInfo.objects.filter(sid=student).values('startlevelid')
            data_fromdb = Classlesson.objects.filter(clclassname=classname).values('clcoursewarename')
            data_dict=ValuesQuerySetToDict(data_fromdb)
            for item in data_dict:
                temp_item_cate = ValuesQuerySetToDict(Lesson.objects.filter(coursewarename=item['clcoursewarename']).values('lesson'))
                delete_repdictkey_long =[]
                delete_repdictkey_short =[]
                for repitem in temp_item_cate:
                    for key in repitem:
                        delete_repdictkey_long.append(repitem[key])
                delete_repdictkey_short = list(set(delete_repdictkey_long))
                delete_repdictkey = []
                for delete_tmp in delete_repdictkey_short:
                    #print delete_tmp
                    temp_dict_name = {}
                    temp_array_lesson = []
                    temp_dict_name['课程分类名'] = delete_tmp
                    lesson_book = ValuesQuerySetToDict(Lesson.objects.filter(coursewarename=item['clcoursewarename'],lesson=delete_tmp).values())
                    temp_array_lesson.append(lesson_book)
                    temp_dict_name['资料'] = temp_array_lesson
                    delete_repdictkey.append(temp_dict_name)
                #print delete_repdictkey
                delete_repdictkey123123 = ValuesQuerySetToDict(delete_repdictkey)
                
                item['课程资料'] = delete_repdictkey
        
        else:
            retrst['result'] = -1
            retrst['errmsg'] = '错误,无效的dataid'
            return respJson(HttpResponseBadRequest(json.dumps(retrst,  ensure_ascii=False)))
        
        retrst['result'] = 0
        retrst['content'] = ValuesQuerySetToDict(data_fromdb)
        #retrst['content'] = student_fromdb #json.dumps(student_fromdb,ensure_ascii=False, cls=awooaJSONEncoder)
        #return HttpResponse(json.dumps(retrst,  ensure_ascii=False, cls=awooaJSONEncoder))
        return respJson(HttpResponse(json.dumps(retrst,  ensure_ascii=False, cls=awooaJSONEncoder)))
    
    elif type == '4':
        """
        type=4 下载文件
        """
        filepath=os.path.join(settings.MEDIA_ROOT+'/Lesson', request.GET['filename'])
        filename=request.GET['filename']
        #downloadsize=request.GET['downloadsize']
        filesize=os.path.getsize(filepath)
        startthistime=0
        wrapper=FileWrapper(file(filepath))
        response=HttpResponse(wrapper,content_type='application/octet-stream')
        #response=HttpResponse(wrapper,mimetype='application/octet-stream')
        response['Content-Length']=filesize
        response['Accept-Ranges']=bytes
        #response['Content-Range']=bytes downloadsize-filesize/filesize
        response['Content-Disposition'] = 'attachment; filename = %s' % filename
        return response

    elif type == '5':
        """
        获取班级编组情况,返回编组班级的人员信息
        """
        gid=request.GET['gid']
        sid=request.GET['student']
        rtn_menu={}
        enToCn={}
        submenu_from_db_myname={}
        submenu_from_db_myname_array=[]
        numberOfStudent=0
        submenu_from_db=Classgroup.objects.filter(gid=gid).values('classname')
        data_dict=ValuesQuerySetToDict(submenu_from_db)
        """
        此处的for循环，通过班级名字查找出对应的班级里面所有人的信息。
        """
        for item in data_dict:
            submenu_from_db=StudentInfo.objects.filter(startlevelid=item['classname']).values('sid','nickname','sex','email','telnumber1',
            'telnumber2','qqnumber','mmnumber','companyname','positionname','photo','startlevelid').order_by("nickname")
            sub_data_dict=ValuesQuerySetToDict(submenu_from_db)
            """
            此处的for循环，将返回的数据里面的英文健值换为中文健值。
            """
            for itemcn in sub_data_dict:
                itemcn['学号'] = itemcn['sid']
                del itemcn['sid']
                itemcn['姓名'] = itemcn['nickname']
                del itemcn['nickname']
                itemcn['性别'] = itemcn['sex']
                del itemcn['sex']
                itemcn['手机1'] = itemcn['telnumber1']
                del itemcn['telnumber1']
                itemcn['手机2'] = itemcn['telnumber2']
                del itemcn['telnumber2']
                itemcn['QQ'] = itemcn['qqnumber']
                del itemcn['qqnumber']
                itemcn['微信'] = itemcn['mmnumber']
                del itemcn['mmnumber']
                itemcn['单位'] = itemcn['companyname']
                del itemcn['companyname']
                itemcn['职位'] = itemcn['positionname']
                del itemcn['positionname']
                itemcn['班级'] = itemcn['startlevelid']
                del itemcn['startlevelid']
                itemcn['照片'] = itemcn['photo']
                del itemcn['photo']
                if(itemcn['学号'] ==sid):
                    """
                    此处注意数组与字典的转换问题
                    """
                    submenu_from_db_myname_dict=itemcn
                    submenu_from_db_myname_array.insert(0,submenu_from_db_myname_dict)
                    submenu_from_db_myname['list'] = submenu_from_db_myname_array
                    submenu_from_db_myname['section'] = '我自己'
                numberOfStudent+=1 #统计学生人数
            tmpvariable=sub_data_dict
            item['list']=tmpvariable
            item['section']=item['classname']
            del item['classname']
        rtn_menu=data_dict
        retrst['count'] = numberOfStudent
        retrst['servertime'] = getServerTime()
        """
        对返回的数组进行排序，保证返回的第一个是用户自己的信息，接着是用户所在班级的学员信息
        """
        retrst['content'] = rtn_menu
        retrst['content'].insert(0,submenu_from_db_myname) #将本人的信息插到返回信息的最前面

        return respJson(HttpResponse(json.dumps(retrst,ensure_ascii=False)))
    
    elif type == '6':
        """
        type=6 下载图片
        """
        filepath=os.path.join(settings.MEDIA_ROOT+'/Student_photo', request.GET['filename'])
        filename=request.GET['filename']
        filesize=os.path.getsize(filepath)
        downloadsize=filesize
        startthistime=0
        wrapper=FileWrapper(file(filepath))
        #response=HttpResponse(wrapper,content_type='application/octet-stream')
        response=HttpResponse(wrapper,mimetype='application/octet-stream')
        response['Content-Length']=os.path.getsize(filepath)
        response['Content-Disposition'] = 'attachment; filename = %s' % filename
        return response
    
    else:
        return HttpResponseBadRequest('GET参数错误，非法type值')
    
    
    
    
    
    
#     def readFile(fn, buf_size=262144):
#         f=open(fn,'rb')
#         while True:
#             c=f.read(buf_size)
#             if c:
#                 yield c 
#             else:
#                 break
#         f.close()
#     
#     filename="test.file"
#     response = HttpResponse(readFile(fn=filename))

    
    
    