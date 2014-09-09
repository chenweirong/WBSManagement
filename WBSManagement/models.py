#-*- encoding:UTF-8 -*- 

from django.db import models
from awooautils import geticonlist,getuploadpath
#import dateutil.parser
import datetime
from django.contrib import admin
from django.forms import ModelForm
from django.db.models.signals import post_delete 
import os
_list_of_page=30

"""
系统设置，包括菜单，帮助信息。
"""

class FirstLevelMenu(models.Model):
    menuid=models.IntegerField(primary_key=True,verbose_name='一级菜单ID')
    icon=models.CharField(max_length=30,choices=geticonlist(),verbose_name='图标')
    menuname=models.CharField(max_length=50,verbose_name='菜单名称')

    def __unicode__(self):
        return  u'%s %s' % (self.menuid,self.menuname)
    class Meta:
        verbose_name='一级菜单'
        verbose_name_plural=verbose_name
    
class SecondLevelMenu(models.Model):
    firstlevelmenuid=models.ForeignKey(FirstLevelMenu,verbose_name='所属一级菜单')
    menuid=models.IntegerField(verbose_name='二级菜单ID')
    icon=models.CharField(max_length=30,choices=geticonlist(),verbose_name='图标')
    menuname=models.CharField(max_length=50,verbose_name='二级菜单名称')
    url=models.CharField(max_length=200,null=True,blank=True,verbose_name='URL')
    
    def __unicode__(self):
        return u'%s %s %s' % (self.firstlevelmenuid,self.menuid,self.menuname)
    class Meta:
        verbose_name='二级菜单'
        verbose_name_plural=verbose_name

class AboutHelp(models.Model):
    title=models.CharField(max_length=100,verbose_name='标题')
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='帮助信息'
        verbose_name_plural=verbose_name
            
"""
班级和学员管理
"""
# 班级
class Classname(models.Model):
    classname=models.CharField(max_length=50,verbose_name='班级名称',primary_key=True)
    startym=models.DateField(verbose_name='开班时间')
    endym=models.DateField(verbose_name='毕业时间')
    dscpt=models.CharField(max_length=500,verbose_name='班级描述',blank=True)
    def __unicode__(self):
        return u'%s'%(self.classname)
    class Meta:
        verbose_name='班级'
        verbose_name_plural=verbose_name
        
class ClassnameAdmin(admin.ModelAdmin):     
    list_display = ('classname', 'startym','endym','dscpt')
    search_fields = ('classname',) #显示搜索栏，此处设置为可用‘学号’、‘姓名’进行搜索

#学员信息
class StudentInfo(models.Model):
    startlevelid=models.ForeignKey(Classname,verbose_name='班级')
    sid=models.CharField(max_length=20,verbose_name='学号',primary_key=True)
    nickname=models.CharField(max_length=30,verbose_name='学生名字')
    sex=models.CharField(max_length=20,choices=(('M','男'),('F','女'),),default=(('M','男'),),verbose_name='性别')
    nation=models.CharField(max_length=32,verbose_name='名族',default='汉族')
    pwd=models.CharField(max_length=32,verbose_name='密码',blank=True)
    email=models.EmailField(verbose_name='学生邮件',blank=True)
    telnumber1=models.CharField(max_length=20,verbose_name='电话号码')
    telnumber2=models.CharField(max_length=20,verbose_name='电话号码1',blank=True)
    qqnumber=models.CharField(max_length=20,verbose_name='QQ号码',blank=True)
    mmnumber=models.CharField(max_length=20,verbose_name='微信号码',blank=True)
    companyname=models.CharField(max_length=100,verbose_name='公司名字',blank=True)
    positionname=models.CharField(max_length=40,verbose_name='职位',blank=True)
    photo=models.ImageField(verbose_name='学生头像',upload_to='Student_photo',blank=True)
    
    def __unicode__(self):
        return  u'%s'%(self.sid)
    class Meta:
        verbose_name='学员信息'
        verbose_name_plural=verbose_name
        
#班级活动
class ClassActivities(models.Model):
    classname=models.ForeignKey(Classname,verbose_name='班级')
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    photo=models.ImageField('活动照片',upload_to=getuploadpath(strtype='ClassActivities_photo'),blank=True)
    title=models.CharField(max_length=100,verbose_name='活动标题')
    dscpt=models.TextField(verbose_name='活动内容',blank=True)
    urladdr=models.FileField(upload_to='ClassActivities_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s %s'%(self.classname,self.title)
    class Meta:
        verbose_name='班级活动'
        verbose_name_plural=verbose_name

#班级编组
class Classgroup(models.Model):
    gid=models.CharField(max_length=100,verbose_name='编组编号',primary_key=True)
    classname=models.ManyToManyField(Classname,verbose_name=u'班级')
    def __unicode__(self):
        return u'%s'%(self.gid)
    class Meta:
        verbose_name='班级编组'
        verbose_name_plural=verbose_name
        
class ClassgroupAdmin(admin.ModelAdmin):
    list_display = ('gid',)
    #如果搜索栏搜索的的是一个外键，需要采取 "本表外键字段__外键所在表需查询字段"的格式进行查询，如果"外键所在表需查询字段"依然
    #是一个外键，可以在"外键所在表需查询字段"中嵌套"本表外键字段(此处为外键的对应字段)__外键所在表需查询字段"的格式进行继续查询，
    #下面的'clcoursewarename__coursewarename__classlessontype'即是这种查询方式。
    search_fields = ('classname__classname','gid') #显示搜索栏 
    list_filter = ('gid',) #显示右侧的过滤器，遵循和搜索栏一样得规则   
    filter_horizontal = ('classname',)
#发布提醒
class Alarm(models.Model):
    classname=models.ForeignKey(Classname,verbose_name='班级')
    studentid=models.CharField(max_length=20,verbose_name='学号',blank=True)
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员')
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    alarmtime=models.DateField(verbose_name='提醒时间')
    title=models.CharField(max_length=100,verbose_name='提醒标题')
    dscpt=models.TextField(verbose_name='提醒内容',blank=True)
    repeatimes=models.IntegerField(max_length=4,verbose_name='重复次数',default='1')
    interval=models.IntegerField(max_length=4,verbose_name='间隔秒数',default='60')
    def __unicode__(self):
        return u'%s %s'%(self.classname,self.title)
    class Meta:
        verbose_name='发布提醒'
        verbose_name_plural=verbose_name 

"""
教学和成绩管理
"""
#课件分类
class Lessontype(models.Model):
    lessontype=models.CharField(max_length=50,verbose_name='分类名称',primary_key=True)
    lessontypenumber=models.IntegerField(verbose_name='分类排序')
    def __unicode__(self):
        return u'%s'%(self.lessontype)
    class Meta:
        verbose_name='课件分类'
        verbose_name_plural=verbose_name
        
#课程名称
class Classlessontype(models.Model):
    classlessontype=models.CharField(max_length=50,verbose_name='课程名称',primary_key=True) 
    classlessontypenumber=models.IntegerField(verbose_name='课程排序')
    startday=models.DateField(verbose_name='课程开始时间')
    endday=models.DateField(verbose_name='课程结束时间')
    def __unicode__(self):
        return u'%s'%(self.classlessontype)
    class Meta:
        verbose_name='课程'
        verbose_name_plural=verbose_name
            
#课件上传
class Lesson(models.Model):
    coursewarename=models.ForeignKey(Classlessontype,verbose_name='课程名称')
    lesson=models.ForeignKey(Lessontype,verbose_name='课件分类')
    lessonnumber=models.IntegerField(verbose_name='课件排序')
    photo=models.ImageField(verbose_name='课件封面',upload_to='Lesson_photo',blank=True)
    fileURL=models.FileField(upload_to='Lesson',verbose_name='文件URL')
    filerealname=models.CharField(max_length=100,verbose_name='文件名')
    #fileextension=models.CharField(max_length=20,verbose_name='文件扩展名')
    filesize=models.CharField(max_length=100,verbose_name='文件大小')
    fileMD5=models.CharField(max_length=32,verbose_name='MD5码')
    def __unicode__(self):
        return u'%s'%(self.coursewarename)
    class Meta:
        verbose_name='课件'
        verbose_name_plural=verbose_name

#课程配置
class Classlesson(models.Model):
    clclassname=models.ForeignKey(Classname,verbose_name='班级',primary_key=True)
    clcoursewarename=models.ManyToManyField(Classlessontype,verbose_name=u'课程名字')
    
    def __unicode__(self):
        return u'%s'%(self.clclassname)
    class Meta:
        verbose_name='课程配置'
        verbose_name_plural=verbose_name
        
class ClasslessonAdmin(admin.ModelAdmin):
    list_display = ('clclassname',)
    search_fields = ('clclassname__classname', 'clcoursewarename__classlessontype') #显示搜索栏 
    list_filter = ('clclassname__classname',) #显示右侧的过滤器，遵循和搜索栏一样得规则
    filter_horizontal = ('clcoursewarename',)
    
#成绩
class Score(models.Model):
    sid=models.ForeignKey(StudentInfo,verbose_name='学号')
    studentname=models.CharField(max_length=30,verbose_name='姓名')
    levelid=models.CharField(max_length=50,verbose_name='班级')
    classlessontype=models.ForeignKey(Classlessontype,verbose_name='课程名称')
    usuallyAbsences=models.CharField(max_length=10,verbose_name='缺勤次数',default='0')
    usuallyLate=models.CharField(max_length=10,verbose_name='迟到次数',default='0')
    usuallyLeaveEarly=models.CharField(max_length=10,verbose_name='早退次数',default='0')
    excamscore=models.CharField(max_length=10,verbose_name='考试成绩',default='0')
    totalScore=models.CharField(max_length=10,verbose_name='总成绩',default='0')
    dscpt=models.CharField(max_length=100,verbose_name='备注',blank=True)
    def __unicode__(self):
        return u'%s'%(self.sid)
    class Meta:
        verbose_name='成绩'
        verbose_name_plural=verbose_name 

#选修管理
class Selective(models.Model):
    name=models.CharField(max_length=100,verbose_name='课程名称')
    lessonnumber=models.IntegerField(verbose_name='课件排序')
    startday=models.DateField(verbose_name='课程开始时间')
    endday=models.DateField(verbose_name='课程结束时间')
    photo=models.ImageField(verbose_name='课件封面',upload_to='Selective_photo',blank=True)
    fileURL=models.FileField(upload_to='Selective_Lesson',verbose_name='文件URL')
    filerealname=models.CharField(max_length=100,verbose_name='文件名')
    #fileextension=models.CharField(max_length=20,verbose_name='文件扩展名')
    filesize=models.CharField(max_length=100,verbose_name='文件大小')
    fileMD5=models.CharField(max_length=32,verbose_name='MD5码')
    def __unicode__(self):
        return u'%s'%(self.name)
    class Meta:
        verbose_name='选修管理'
        verbose_name_plural=verbose_name 
    
#答辩管理  
class Oralefense(models.Model):
    name=models.CharField(max_length=100,verbose_name='答辩题目')
    teachername=models.CharField(max_length=40,verbose_name='指导老师')
    sid=models.ForeignKey(StudentInfo,verbose_name='学号')
    studentname=models.CharField(max_length=30,verbose_name='姓名')
    levelid=models.CharField(max_length=50,verbose_name='班级')
    startday=models.DateField(verbose_name='答辩开始时间')
    endday=models.DateField(verbose_name='答辩结束时间')
    totalScore=models.CharField(max_length=10,verbose_name='成绩',default='0')
    dscpt=models.CharField(max_length=100,verbose_name='备注',blank=True)
    
    def __unicode__(self):
        return u'%s'%(self.name)
    class Meta:
        verbose_name='答辩管理'
        verbose_name_plural=verbose_name 

"""
商学院信息
"""
#院长寄语
class Dean(models.Model):
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s %s'%(self.urladdr,self.appointurl)
    class Meta:
        verbose_name='院长寄语'
        verbose_name_plural=verbose_name

#学院介绍
class Academy(models.Model):
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s %s'%(self.urladdr,self.appointurl)
    class Meta:
        verbose_name='学院介绍'
        verbose_name_plural=verbose_name
    
#联系方式
class Contact(models.Model):
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s %s'%(self.urladdr,self.appointurl)
    class Meta:
        verbose_name='联系方式'
        verbose_name_plural=verbose_name
        
#信息发布
class Information(models.Model):
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    title=models.CharField(max_length=100,verbose_name='标题')
    dscpt=models.TextField(verbose_name='内容',blank=True)
    photo=models.ImageField('标题照片',upload_to=getuploadpath(strtype='School_photo'),blank=True)
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='商学院信息'
        verbose_name_plural=verbose_name

"""
校友管理 Schoolmate
"""
#通知
class Inform(models.Model):
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    title=models.CharField(max_length=100,verbose_name='标题')
    dscpt=models.TextField(verbose_name='内容',blank=True)
    photo=models.ImageField('标题照片',upload_to=getuploadpath(strtype='Schoolmate_photo'),blank=True)
    urladdr=models.FileField(upload_to='Schoolmate_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='通知'
        verbose_name_plural=verbose_name
        
#访谈 
class Interview(models.Model):
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    title=models.CharField(max_length=100,verbose_name='标题')
    dscpt=models.TextField(verbose_name='内容',blank=True)
    photo=models.ImageField('标题照片',upload_to=getuploadpath(strtype='Schoolmate_photo'),blank=True)
    urladdr=models.FileField(upload_to='Schoolmate_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='访谈'
        verbose_name_plural=verbose_name
        
#咨询
class Consult(models.Model):
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    title=models.CharField(max_length=100,verbose_name='标题')
    dscpt=models.TextField(verbose_name='内容',blank=True)
    photo=models.ImageField('标题照片',upload_to=getuploadpath(strtype='Schoolmate_photo'),blank=True)
    urladdr=models.FileField(upload_to='Schoolmate_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='咨询'
        verbose_name_plural=verbose_name

"""
内刊 Journal
"""
#内刊分类
class JournalType(models.Model):
    journaltype=models.CharField(max_length=50,verbose_name='分类名称',primary_key=True)
    journalnumber=models.IntegerField(verbose_name='分类排序')
    def __unicode__(self):
        return u'%s'%(self.journaltype)
    class Meta:
        verbose_name='内刊分类'
        verbose_name_plural=verbose_name
        
#内刊上传
class JournalUpdate(models.Model):
    Journal=models.ForeignKey(JournalType,verbose_name='内刊分类')
    Journalnumber=models.IntegerField(verbose_name='文件排序')
    photo=models.ImageField(verbose_name='内刊封面',upload_to='Journal_photo/%Y/%m/%d',blank=True)
    fileURL=models.FileField(upload_to='Journal',verbose_name='文件URL')
    filerealname=models.CharField(max_length=100,verbose_name='文件名')
    filesize=models.CharField(max_length=100,verbose_name='文件大小')
    fileMD5=models.CharField(max_length=32,verbose_name='MD5码')
    def __unicode__(self):
        return u'%s'%(self.Journal)
    class Meta:
        verbose_name='上传内刊'
        verbose_name_plural=verbose_name
        
#内刊配置
class Journal(models.Model):
    clclassname=models.ForeignKey(Classname,verbose_name='班级')
    Journalname=models.ForeignKey(JournalType,verbose_name='内刊分类')
    def __unicode__(self):
        return u'%s'%(self.Journalname)
    class Meta:
        verbose_name='内刊配置'
        verbose_name_plural=verbose_name
        
class JournalAdmin(admin.ModelAdmin):
    list_display = ('clclassname', 'Journalname')
    #如果搜索栏搜索的的是一个外键，需要采取 "本表外键字段__外键所在表需查询字段"的格式进行查询，如果"外键所在表需查询字段"依然
    #是一个外键，可以在"外键所在表需查询字段"中嵌套"本表外键字段(此处为外键的对应字段)__外键所在表需查询字段"的格式进行继续查询，
    #下面的'clcoursewarename__coursewarename__classlessontype'即是这种查询方式。
    search_fields = ('clclassname__classname', 'Journalname__journaltype') #显示搜索栏 
    list_filter = ('clclassname__classname','Journalname__journaltype',) #显示右侧的过滤器，遵循和搜索栏一样得规则

"""
广告和周边详情
"""
#广告位管理
class PlayInfo(models.Model):
    PlayInfoTitle=models.CharField(max_length=50,verbose_name='广告标题')
    PlayInfoNumber=models.IntegerField(verbose_name='广告位置')
    PlayInfoTime=models.IntegerField(verbose_name='播放时间')
    photo=models.ImageField('广告图片',upload_to=getuploadpath(strtype='Advertisement_photo'),blank=True)
    urladdr=models.FileField(upload_to='School_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.PlayInfoNumber)
    class Meta:
        verbose_name='广告管理'
        verbose_name_plural=verbose_name

#周边信息
class AroundType(models.Model):
    aroundtype=models.CharField(max_length=50,verbose_name='分类名称',primary_key=True)
    aroundnumber=models.IntegerField(verbose_name='分类排序')
    def __unicode__(self):
        return u'%s'%(self.aroundtype)
    class Meta:
        verbose_name='周边信息分类'
        verbose_name_plural=verbose_name
        
class Around(models.Model):
    aroundtype=models.ForeignKey(AroundType,verbose_name='周边信息分类')
    publisher=models.CharField(max_length=50,verbose_name='发布人',default='管理员',blank=True)
    publishtime=models.DateField(verbose_name='发布时间',default=datetime.datetime.now().date)
    title=models.CharField(max_length=100,verbose_name='标题')
    dscpt=models.TextField(verbose_name='内容',blank=True)
    photo=models.ImageField('标题照片',upload_to=getuploadpath(strtype='Around_photo'),blank=True)
    urladdr=models.FileField(upload_to='Around_html',verbose_name='活动详情网页',blank=True,help_text='请将网页及网页相关的文件放在同一文件夹里打包后，选择上传整个压缩包（zip格式）,如果需要链接到特定的网址，请不要填写此项')
    appointurl=models.CharField(max_length=200,verbose_name='指定网址',blank=True,help_text='如果需要链接到特定的网址，请在此输入网址全称（例如：http://www.baidu.com）')
    def __unicode__(self):
        return u'%s'%(self.title)
    class Meta:
        verbose_name='周边信息'
        verbose_name_plural=verbose_name
        
#---------------------------------------------------------------------------------------------------#

"""
CfgPara系统参数，用于全局系统参数设定
"""
class CfgParas(models.Model):
    paraname=models.CharField('系统变量名',max_length=20,primary_key=True)
    paravalue=models.CharField('系统变量值',max_length=200,blank=True,null=True)
    paradscpt=models.CharField('变量说明',max_length=200,blank=True,null=True)
    def __unicode__(self):
        return u'%s-%s'%(self.paraname,self.paradscpt)
    class Meta:
        verbose_name='系统全局参数'
        verbose_name_plural=verbose_name
    
