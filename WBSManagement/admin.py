#-*- encoding:UTF-8 -*- 

from django import forms
from django.db import models
from django.contrib import admin

from WBSManagement.awooautils import AwooaAdminSite
from WBSManagement.models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from WBSManagement.forms import *


WBSManagementAdmin=AwooaAdminSite()
WBSManagementAdmin.register(Group,GroupAdmin)
WBSManagementAdmin.register(User,UserAdmin)
WBSManagementAdmin.register(FirstLevelMenu)
WBSManagementAdmin.register(SecondLevelMenu)


class AboutHelpAdmin(admin.ModelAdmin):
    form=AboutHelpAdminForm
    list_display = ('title','appointurl')
    search_fields = ('title',)
    fields = ('title','urladdr')
WBSManagementAdmin.register(AboutHelp,AboutHelpAdmin)

WBSManagementAdmin.register(Classname,ClassnameAdmin)
    

#此为给 ‘用户信息’ 建立的新类，以实现 ‘用户信息’ 的自定义显示
class StudentInfoAdmin(admin.ModelAdmin):
    form=StudentInfoAdminForm
    list_display = ('sid', 'nickname','startlevelid','telnumber1','positionname','companyname','photo') #分别以‘学号’、‘姓名’、‘班级’列出三栏
    search_fields = ('sid','nickname','telnumber1','telnumber2','startlevelid__classname') #显示搜索栏，此处设置为可用‘学号’、‘姓名’进行搜索
    list_filter = ('startlevelid__classname',)
WBSManagementAdmin.register(StudentInfo,StudentInfoAdmin)

class ClassActivitiesAdmin(admin.ModelAdmin):
    form=ClassActivitiesAdminForm
    list_display = ('classname','publisher','title','publishtime','photo','appointurl') #显示那些项
    search_fields = ('classname__classname','publisher','title') #显示搜索栏，'publishtime'添加后会出错，原因不明。     
    fields = ('classname','title','dscpt','photo','urladdr','appointurl')  #表单中那些项可填写
    list_filter = ('classname__classname','publishtime') #显示右侧的过滤器   
WBSManagementAdmin.register(ClassActivities,ClassActivitiesAdmin)

class AlarmAdmin(admin.ModelAdmin):
    form=AlarmAdminForm
    list_display = ('classname','publisher','title','publishtime','alarmtime')
    list_filter = ('classname__classname','publishtime') #显示右侧的过滤器
    search_fields = ('classname__classname','publisher','title','studentid') #显示搜索栏，'publishtime'添加后会出错，原因不明。
    #raw_id_fields = ('studentid',)
    fields = ('classname','studentid','alarmtime','title'
              ,'dscpt','repeatimes','interval')  
WBSManagementAdmin.register(Alarm,AlarmAdmin)
WBSManagementAdmin.register(Classgroup,ClassgroupAdmin)


WBSManagementAdmin.register(Lessontype)
WBSManagementAdmin.register(Classlessontype)

class LessonAdmin(admin.ModelAdmin):
    form=LessonAdminForm
    list_display = ('coursewarename','lesson','lessonnumber','filerealname','filesize','fileMD5','fileURL')
    search_fields = ('coursewarename__classlessontype', 'lesson__lessontype','filerealname') #显示搜索栏  
    fields = ('coursewarename','lesson','lessonnumber','fileURL')
    list_filter = ('lesson__lessontype',) #显示右侧的过滤器
WBSManagementAdmin.register(Lesson,LessonAdmin)

WBSManagementAdmin.register(Classlesson,ClasslessonAdmin)

class ScoreAdmin(admin.ModelAdmin):
    form=ScoreAdminForm
    list_display = ('sid','studentname','levelid','classlessontype','usuallyAbsences','usuallyLate',
                    'usuallyLeaveEarly','excamscore','totalScore','dscpt')
    #显示搜索栏
    search_fields = ('sid__sid','classlessontype__classlessontype','studentname')  
    raw_id_fields = ('sid',)
    list_filter = ('levelid','classlessontype__classlessontype',) #显示右侧的过滤器
    #排序
    #ordering = ('sid',) 
    #调整字段得显示顺序，没添加到此队列得字段，将不允许被编辑  
    fields = ('sid','classlessontype','usuallyAbsences','usuallyLate','usuallyLeaveEarly'
              ,'excamscore','totalScore','dscpt') 
    #设置只读字段，需要注意的是，该字段只接受元组或列表，也就是不能只存在一个，如果只让一个字段只读，在引号后面加个逗号“,”即可
    #readonly_fields=('studentname','levelid',)
    #prepopulated_fields = {"studentname": ("sid",)}
WBSManagementAdmin.register(Score,ScoreAdmin)

class SelectiveAdmin(admin.ModelAdmin):
    form=SelectiveAdminForm
    list_display = ('name','startday','endday','photo','filerealname','filesize','fileMD5','fileURL')
    search_fields = ('name','filerealname',) 
    fields = ('name','lessonnumber','startday','endday','photo','fileURL')
WBSManagementAdmin.register(Selective,SelectiveAdmin)

class OralefenseAdmin(admin.ModelAdmin):
    form=OralefenseAdminForm
    list_display = ('name','teachername','sid','studentname','levelid', 'startday','endday',
                    'totalScore','dscpt')
    raw_id_fields = ('sid',)
    search_fields = ('name','sid','studentname','levelid','teachername')
    fields = ('name','teachername','sid','startday','endday','totalScore','dscpt') 
    list_filter = ('name','levelid',)
WBSManagementAdmin.register(Oralefense,OralefenseAdmin)

class DeanAdmin(admin.ModelAdmin):
    form=DeanAdminForm
    list_display = ('urladdr', 'appointurl')
WBSManagementAdmin.register(Dean,DeanAdmin)

class AcademyAdmin(admin.ModelAdmin):
    form=AcademyAdminForm
    list_display = ('urladdr', 'appointurl')
WBSManagementAdmin.register(Academy,AcademyAdmin)

class ContactAdmin(admin.ModelAdmin):
    form=ContactAdminForm
    list_display = ('urladdr', 'appointurl')
WBSManagementAdmin.register(Contact,ContactAdmin)

class InformationAdmin(admin.ModelAdmin):
    form=InformationAdminForm
    list_display = ('title','publishtime','publisher','photo','appointurl')
    search_fields = ('title','publisher')
    fields = ('title','dscpt','photo','urladdr','appointurl') 
    list_filter = ('publishtime',)
WBSManagementAdmin.register(Information,InformationAdmin)

class InformAdmin(admin.ModelAdmin):
    form=InformAdminForm
    list_display = ('title','publishtime','publisher','photo','appointurl')
    search_fields = ('title','publisher')
    fields = ('title','dscpt','photo','urladdr','appointurl') 
    list_filter = ('publishtime',)
WBSManagementAdmin.register(Inform,InformAdmin)

class InterviewAdmin(admin.ModelAdmin):
    form=InterviewAdminForm
    list_display = ('title','publishtime','publisher','photo','appointurl')
    search_fields = ('title','publisher')
    fields = ('title','dscpt','photo','urladdr','appointurl') 
    list_filter = ('publishtime',)
WBSManagementAdmin.register(Interview,InterviewAdmin)

class ConsultAdmin(admin.ModelAdmin):
    form=ConsultAdminForm
    list_display = ('title','publishtime','publisher','photo','appointurl')
    search_fields = ('title','publisher')
    fields = ('title','dscpt','photo','urladdr','appointurl') 
    list_filter = ('publishtime',)
WBSManagementAdmin.register(Consult,ConsultAdmin)


WBSManagementAdmin.register(JournalType)

class JournalUpdateAdmin(admin.ModelAdmin):
    form=JournalUpdateAdminForm
    list_display = ('Journal','Journalnumber','filerealname','fileMD5','filesize','fileURL')
    search_fields = ('Journal__Journaltype','filerealname') #显示搜索栏  
    fields = ('Journal','Journalnumber','photo','fileURL')
    list_filter = ('Journal__journaltype',) #显示右侧的过滤器
WBSManagementAdmin.register(JournalUpdate,JournalUpdateAdmin)

WBSManagementAdmin.register(Journal,JournalAdmin)

class PlayInfoAdmin(admin.ModelAdmin):
    form=PlayInfoAdminForm
    list_display = ('PlayInfoTitle','PlayInfoNumber','PlayInfoTime','photo','appointurl')
    fields = ('PlayInfoTitle','PlayInfoNumber','PlayInfoTime','photo','urladdr','appointurl')
WBSManagementAdmin.register(PlayInfo,PlayInfoAdmin)

WBSManagementAdmin.register(AroundType)

class AroundAdmin(admin.ModelAdmin):
    form=AroundAdminForm
    list_display = ('title','publishtime','publisher','aroundtype','photo','appointurl')
    search_fields = ('title','publisher') #显示搜索栏  
    fields = ('aroundtype','title','dscpt','photo','urladdr')
    list_filter = ('aroundtype__aroundtype',) #显示右侧的过滤器
WBSManagementAdmin.register(Around,AroundAdmin)

"""
凡是需要重新定义不同于默认模版显示的字段，都可以按照如下方式，定义并注册
"""
class CfgParasAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField:{'widget':TextInput(attrs={'size':'100'})},
#         }
    def formfield_for_dbfield(self,db_field,**kwargs):
        field=super(CfgParasAdmin,self).formfield_for_dbfield(db_field,**kwargs)
        if db_field.name == 'paravalue':
            field.widget = forms.TextInput(attrs={'size':'80'})
        elif db_field.name == 'paradscpt':
            field.widget = forms.Textarea(attrs={'rows':8,'cols':80})
        return field


WBSManagementAdmin.register(CfgParas,CfgParasAdmin)




