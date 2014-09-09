#-*- encoding:UTF-8 -*- 
import os, tempfile, zipfile, glob, re
from django import forms
from WBSManagement.models import *
from WBSManagement.views import *
from WBSManagement.awooautils import getStringMd5
from WBSManagement.awooautils import getFileMd5

#from WBSManagement import threadlocals
#from django.contrib.auth.models import User
import socket
#LOCALIP='http://127.0.0.1:8000'
"""
密码算法：数字盘码 14789 就是大L
cid码：studentid + 数字盘码 + 系统时间 的字符串md5码
"""
# class StudentInfoAdminForm(forms.ModelForm):
#     pwdChoices=(('Keep','不更新密码'),('Refresh','重置为初始密码'),)
#     pwd=forms.ChoiceField(choices=pwdChoices)
#     
#     def save(self, commit=True):
#         studentinfo = super(StudentInfoAdminForm, self).save(commit=False)
# 
#         if studentinfo.pwd == 'Refresh':
#             #studentinfo.pwd = getStringMd5(u'%s%s'%(studentinfo.sid,'14789'))
#             studentinfo.pwd = '14789'
#         else:
#             #不可更新pwd字段
#             studentinfo.pwd = self.initial['pwd']
#         if commit:
#             studentinfo.save()
#         return studentinfo
#         
#     
#     class Meta:
#         model=StudentInfo
#         #exclude=('pwd',)


"""
此函数为获取上传的解压文件中的网页，设置为本地可访问的静态网站。
"""
def CreatWebPage(filePath,webPagePath,staticPath):
    try:
            zipFiles = zipfile.ZipFile(filePath,'r')
            fileurl=os.path.splitext(filePath)[0]#获取解压路径
            zipFiles.extractall(fileurl)
            zipFiles.close()
            os.remove(filePath)
             
            find_file=re.compile(r".htm$")
            find_path=os.path.splitext(filePath)[0]
            find_walk=os.walk(find_path)
            point=0
            for path,dirs,files in find_walk:
                for file in files:
                    if find_file.search(file):
                        if point==0:
                            point=1
                            #webPagePath.appointurl =LOCALIP+staticPath+'%s'%os.path.basename(path)+'/'+'%s'%os.path.basename(file)
                            webPagePath.appointurl =staticPath+'%s'%os.path.basename(path)+'/'+'%s'%os.path.basename(file)
            if point==0:        
                find_file=re.compile(r".html$")
                find_path=os.path.splitext(filePath)[0]
                find_walk=os.walk(find_path)
                for path,dirs,files in find_walk:
                    for file in files:
                        if find_file.search(file):
                            if point==0:
                                point=1
                                #webPagePath.appointurl =LOCALIP+staticPath+'%s'%os.path.basename(path)+'/'+'%s'%os.path.basename(file)
                                webPagePath.appointurl =staticPath+'%s'%os.path.basename(path)+'/'+'%s'%os.path.basename(file)
    except:
        pass

        
class AboutHelpAdminForm(forms.ModelForm):
    def save(self, commit=True):
        aboutHelp = super(AboutHelpAdminForm, self).save(commit=False)
        aboutHelp.save()
        tempFilePath='/media/AboutHelp_html/'
        CreatWebPage(aboutHelp.urladdr.path,aboutHelp,tempFilePath)
        if commit:
            aboutHelp.save()
        return aboutHelp
    class Meta:
        model=AboutHelp
        
class StudentInfoAdminForm(forms.ModelForm):
    def save(self, commit=True):
        studentInfo = super(StudentInfoAdminForm, self).save(commit=False)
        if studentInfo.sex=='M':
            studentInfo.sex='男'
        else:
            studentInfo.sex='女'
        if commit:
            studentInfo.save()
        return studentInfo
    class Meta:
        model=StudentInfo
        
class ClassActivitiesAdminForm(forms.ModelForm):
    def save(self, commit=True):
        classActivities = super(ClassActivitiesAdminForm, self).save(commit=False)
        classActivities.save()
        classActivities.publisher = GetUserName()
        tempFilePath='/media/ClassActivities_html/'
        CreatWebPage(classActivities.urladdr.path,classActivities,tempFilePath)
        if commit:
            classActivities.save()
        return classActivities
    class Meta:
        model=ClassActivities   
        
class AlarmAdminForm(forms.ModelForm):
    def save(self, commit=True):
        alarm = super(AlarmAdminForm, self).save(commit=False)
        alarm.save()
        alarm.publisher = GetUserName()
        if commit:
            alarm.save()
        return alarm
    class Meta:
        model=Alarm   
        
class LessonAdminForm(forms.ModelForm):
    def save(self, commit=True):
        lesson = super(LessonAdminForm, self).save(commit=False)
        """
        通过判断MD5码的变化，更新文件真实的名字，否则在重新进入表，不做任何修改的条件下，真实文件名被django默认保存为路径。
        """
        if lesson.fileMD5:
            if (lesson.fileMD5 == getFileMd5(os.path.abspath(lesson.fileURL.path))):
                pass
            else:
                lesson.filerealname=lesson.fileURL.name
                lesson.save() #先保存，以便获取文件路径。
                lesson.filesize=lesson.fileURL.size
                lesson.fileMD5= getFileMd5(os.path.abspath(lesson.fileURL.path))
        else:
            lesson.filerealname=lesson.fileURL.name
            lesson.save()
            lesson.filesize=lesson.fileURL.size
            lesson.fileMD5= getFileMd5(os.path.abspath(lesson.fileURL.path))   

        if commit:
            lesson.save()
        return lesson
    class Meta:
        model=Lesson
        
class ScoreAdminForm(forms.ModelForm):
    def save(self, commit=True):
        score = super(ScoreAdminForm, self).save(commit=False)
        score.studentname = StudentInfo.objects.get(sid=score.sid).nickname
        score.levelid = StudentInfo.objects.get(sid=score.sid).startlevelid
        if commit:
            score.save()
        return score
    class Meta:
        model=Score
        
class SelectiveAdminForm(forms.ModelForm):
    def save(self, commit=True):
        selective = super(SelectiveAdminForm, self).save(commit=False)
        selective.filerealname=selective.fileURL.name
        selective.filesize=selective.fileURL.size
        selective.fileMD5=getStringMd5(selective.fileURL.path)
        if commit:
            selective.save()
        return selective
    class Meta:
        model=Selective
        
class OralefenseAdminForm(forms.ModelForm):
    def save(self, commit=True):
        oralefense = super(OralefenseAdminForm, self).save(commit=False)
        oralefense.studentname = StudentInfo.objects.get(sid=oralefense.sid).nickname
        oralefense.levelid = StudentInfo.objects.get(sid=oralefense.sid).startlevelid
        if commit:
            oralefense.save()
        return oralefense
    class Meta:
        model=Oralefense

class DeanAdminForm(forms.ModelForm):
    def save(self, commit=True):
        dean = super(DeanAdminForm, self).save(commit=False)
        dean.save()
        tempFilePath='/media/School_html/'
        CreatWebPage(dean.urladdr.path,dean,tempFilePath)
        if commit:
            dean.save()
        return dean
    class Meta:
        model=Dean 
        
class AcademyAdminForm(forms.ModelForm):
    def save(self, commit=True):
        academy = super(AcademyAdminForm, self).save(commit=False)
        academy.save()
        tempFilePath='/media/School_html/'
        CreatWebPage(academy.urladdr.path,academy,tempFilePath)
        if commit:
            academy.save()
        return academy
    class Meta:
        model=Academy
        
class ContactAdminForm(forms.ModelForm):
    def save(self, commit=True):
        contact = super(ContactAdminForm, self).save(commit=False)
        contact.save()
        tempFilePath='/media/School_html/'
        CreatWebPage(contact.urladdr.path,contact,tempFilePath)
        if commit:
            contact.save()
        return contact
    class Meta:
        model=Contact

class InformationAdminForm(forms.ModelForm):
    def save(self, commit=True):
        information = super(InformationAdminForm, self).save(commit=False)
        information.save()
        information.publisher=GetUserName()
        tempFilePath='/media/School_html/'
        CreatWebPage(information.urladdr.path,information,tempFilePath)
        if commit:
            information.save()
        return information
    class Meta:
        model=Information
        
class InformAdminForm(forms.ModelForm):
    def save(self, commit=True):
        inform = super(InformAdminForm, self).save(commit=False)
        inform.save()
        inform.publisher=GetUserName()
        tempFilePath='/media/Schoolmate_html/'
        CreatWebPage(inform.urladdr.path,inform,tempFilePath)
        if commit:
            inform.save()
        return inform
    class Meta:
        model=Inform
        
class InterviewAdminForm(forms.ModelForm):
    def save(self, commit=True):
        interview = super(InterviewAdminForm, self).save(commit=False)
        interview.save()
        interview.publisher=GetUserName()
        tempFilePath='/media/Schoolmate_html/'
        CreatWebPage(interview.urladdr.path,interview,tempFilePath)
        if commit:
            interview.save()
        return interview
    class Meta:
        model=Interview
        
class ConsultAdminForm(forms.ModelForm):
    def save(self, commit=True):
        consult = super(ConsultAdminForm, self).save(commit=False)
        consult.save()
        consult.publisher=GetUserName()
        tempFilePath='/media/Schoolmate_html/'
        CreatWebPage(consult.urladdr.path,consult,tempFilePath)
        if commit:
            consult.save()
        return consult
    class Meta:
        model=Consult
        
class JournalUpdateAdminForm(forms.ModelForm):
    def save(self, commit=True):
        journal = super(JournalUpdateAdminForm, self).save(commit=False)
        if journal.fileMD5:
            if (journal.fileMD5 == getFileMd5(os.path.abspath(journal.fileURL.path))):
                pass
            else:
                journal.filerealname=journal.fileURL.name
                journal.save() #先保存，以便获取文件路径。
                journal.filesize=journal.fileURL.size
                journal.fileMD5= getFileMd5(os.path.abspath(journal.fileURL.path))
        else:
            journal.filerealname=journal.fileURL.name
            journal.save()
            journal.filesize=journal.fileURL.size
            journal.fileMD5= getFileMd5(os.path.abspath(journal.fileURL.path))
        if commit:
            journal.save()
        return journal
    class Meta:
        model=JournalUpdate
        
class PlayInfoAdminForm(forms.ModelForm):
    def save(self, commit=True):
        playinfo = super(PlayInfoAdminForm, self).save(commit=False)
        playinfo.save()
        tempFilePath='/media/School_html/'
        CreatWebPage(playinfo.urladdr.path,playinfo,tempFilePath)
        if commit:
            playinfo.save()
        return playinfo
    class Meta:
        model=PlayInfo
        
class AroundAdminForm(forms.ModelForm):
    def save(self, commit=True):
        around = super(AroundAdminForm, self).save(commit=False)
        around.save()
        around.publisher=GetUserName()
        tempFilePath='/media/Around_html/'
        CreatWebPage(around.urladdr.path,around,tempFilePath)
        if commit:
            around.save()
        return around
    class Meta:
        model=Around
