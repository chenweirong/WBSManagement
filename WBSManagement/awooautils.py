#!/usr/bin/env python
#coding=utf-8

import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import os.path

_lower_cases="abcdefghjkmnpqrstuvwxy"
_upper_cases=_lower_cases.upper()
_numbers=''.join(map(str,range(3,10)))
init_cases=''.join((_lower_cases,_upper_cases,_numbers))
font_path= os.path.join(os.path.dirname(os.path.abspath(__file__)),'Arial.ttf')

def create_verifycode(size=(120,20),
                      chars=init_cases,
                      image_type="GIF",
                      mode="RGB",
                      bg_color=(255,255,255),
                      fg_color=(0,0,255),
                      font_size=20,
                      font_type=font_path,
                      length=4,
                      draw_lines=True,
                      n_line=(1,2),
                      draw_points=True,
                      point_chance=2,
                      ):
    width,height=size
    img=Image.new(mode,size, bg_color)
    draw=ImageDraw.Draw(img)
    
    def get_chars():
        return random.sample(chars,length)
    
    def create_lines(n=2):
        for i  in range(n):
            begin=(random.randint(0,size[0]),random.randint(0,size[1]))
            end=(random.randint(0,size[0]),random.randint(0,size[1]))
            draw.line([begin,end], fill=(0,0,255))
    
    def create_points():
        chance=min(100,max(0,int(point_chance)))
        
        for w in xrange(width):
            for h in xrange(height):
                tmp=random.randint(0,100)
                if tmp>100-chance:
                    draw.point([w,h], fill=(0,0,0))
                    
    def create_strs():
        c_chars=get_chars()
        strs='%s'%' '.join(c_chars)
        
        font=ImageFont.truetype(font_type,font_size)
        font_width,font_height=font.getsize(strs)
        
        draw.text(((width-font_width)/5,(height-font_height)/5), strs, fill=fg_color, font=font)
        return ''.join(c_chars)

    if draw_lines:
        create_lines(n=3)
    
    if draw_points:
        create_points()
        
    strs=create_strs()
    
    params=[1-float(random.randint(1,2))/100,
            0,
            0,
            0,
            1-float(random.randint(1,10))/100,
            float(random.randint(1,2))/500,
            0.001,
            float(random.randint(1,2))/500,
            ]
    img=img.transform(size, Image.PERSPECTIVE, params)
    img=img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    
    return img,strs

import settings
"""
取icon.css文件里面所有项目，用作数据表的选择项
"""
def geticonlist():
    rs=[]
    cssfilepath=os.path.join(settings.PROJECT_PATH,'static/js/themes/icon.css').replace('\\','/')
    try:
        fin=open(cssfilepath,'rt')
    except IOError,e:
        raise e
    while True:
        line=fin.readline()
        if not line: break;
        if line.startswith('.icon'):
            stra=line.split('{')[0].strip('.')
            rs.append((stra,stra))
    return rs

from datetime import datetime
"""
动态文件上传的目录，取当天日期作为上传目录中部分，避免大量文件挤在一个目录里面
"""
def getuploadpath(strtype):
    date=datetime.now().strftime('%Y%m%d')
    return u'%s/%s'%(strtype,date)

"""
取utc当前时间与1970-01-01 00:00:00的时间差的总秒数除以600
"""
def getServerTime():
    utcnow=datetime.utcnow()
    t1970=datetime(1970,1,1,0,0,0,0)
    timespan=utcnow-t1970
    return u'%s'%long(timespan.total_seconds()/600)
    
    


"""
继承AdminSite，修改admin的默认部分路径，删除admin路径，使用自行定义的（在urls文件里面)
"""
from django.contrib.admin import AdminSite
class AwooaAdminSite(AdminSite):
    def get_urls(self):
        from django.conf.urls import patterns,url
        urls=super(AwooaAdminSite,self).get_urls()
        """
        urls += patterns('',
            url(r'myview/$',self.admin_view(someview)),
        """
        del urls[0]
        return urls
    

"""
处理 md5
"""
import hashlib
import os
def getStringMd5(str):
    return hashlib.md5(str).hexdigest().upper()
"""
获得文件md5, filename须为全路径文件名
"""
def getFileMd5(filename):
    if not os.path.isfile(filename):
        return 
    myhash=hashlib.md5()
    f=file(filename,'rb')
    while(True):
        b=f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest().upper()


"""
字符串时间密码验证
根据字符串明码、密码判断是否符合
明码计算3个时间数字，前后10分钟的数字生成密码进行判断
"""
def checkStudentPwd(sid, pwd,encodedstr):
        
    utcnow=datetime.utcnow()
    t1970=datetime(1970,1,1,0,0,0,0)
    timespan=utcnow-t1970
    curkey=u'%s%d'%(sid,long(pwd) * long(timespan.total_seconds()/600))
    bf10minskey=u'%s%d'%(sid, long(pwd) * long(timespan.total_seconds()/600-1))
    af10minskey=u'%s%d'%(sid, long(pwd) * long(timespan.total_seconds()/600+1))
    
    if encodedstr == getStringMd5(curkey):
        return True
    elif encodedstr == getStringMd5(bf10minskey):
        return True
    elif encodedstr == getStringMd5(af10minskey):
        return True
    else:
        return False
    
"""
将HttpResponse的ContentType设置为Json
"""
def respJson(resp):
    resp['content-type'] = 'application/json;charset=UTF-8'
    return resp ;