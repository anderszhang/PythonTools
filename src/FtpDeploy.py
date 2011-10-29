#-*- coding: UTF-8 -*
'''
Created on 2011-9-29
 代码自动部署程序
@author: anderszhang
email:anderszhang@gmail.com
'''
import os
import time
from ftplib import FTP
import shutil
#要部署的文件位置
servers=[{'type':'FTP',
          'name':'UAT',
          'ip':'11.251.104.11',
          'username':'branch',
          'password':'branch',
          'serverDataFolder':'/home/branch/tmp',
          'severWebFolder':'/home/branch/tmp',
          'webDataFolder':'',
          'bakFolder':'/home/branch/tmp/bak'
          },
         {'type':'LOCAL',
          'name':'UAT_DISPLAY',
          'serverDataFolder':'/home/branch/tmp',
          'severWebFolder':'/home/branch/tmp',
        }]

UPDATE_FILE='uploadFiles.txt'
LOCAL_BAKFOLDER =""
#将文件上传至服务器
def uploadFile(server):
    ftp = FTP(server['ip']);
    ftp.login(server['username'], server['password'])
    ftp.cwd(server['serverDataFolder']) 
    confFile = open(os.path.join(os.getcwd(),UPDATE_FILE)) #读取更新文件列表
    print ftp.pwd()
    lines = confFile.readlines()
    for l in lines: #处理文件的每一行
        l = l.rstrip() #去掉行首和行尾的空格,及行尾的回车符
        #如果没有注释掉,且文件存在
        if l.find('#')==-1 and os.path.exists(l):
            (path,file)= os.path.split(l); #将路径分的成目录和文件名
            if path.find('resource') > -1: #资源文件判断
                fileDir = path[path.find('resource'):] #截取路径
            elif path.find('webapps/branch') >-1: #web 文件判断,本地测试使用WebRoot
                fileDir = path[path.find('resource'):] 
            fileDir = fileDir.replace("\\",'/') #将win风格的路径转为Unix风格
            ftp.cwd(fileDir) #切换至服务器相应目录
            ftpMkdir(ftp,'')
            f = open(l)
            ftp.storlines('STOR '+file,f) #上传文件至服务器
            ftp.cwd(server['serverDataFolder']) #切换至数据文件根目录
            f.close()
    ftp.close()
    
#本地磁盘复制
def copy2LocalDisk(path):
    shutil.copy2(path, "")
    
#回滚至版本
def rollback(version):
    pass

#检查ftp服务器文件夹是否存在,不存在就建一个
def ftpMkdir(ftp,path):
    existFlag = ftp.dir('/home/branch/tmp/bak')
    if not existFlag :
        ftp.mkd('/home/branch/tmp/bak');

#在本地写一个日志文件
def writeLog(filName):
    p = os.path.curdir
    logName = '%s_update.log' %(time.strftime('%Y%m%d'))
    f = open(os.path.join(p,logName),'a')  #以追加方式打开文件
    print p
    f.write("aaa")    #写入文件
    f.write("\n")
    f.close();

def getVersion():
    pass;
#将文件移至备份文件夹
def bakupFile(ftp,file):
    # Ftp日期备份
    ftp.cwd("") #切换至备份目录
    d = time.strftime('%Y%m%d')
    ftpMkdir(ftp,d)   #如果当时日期的备份日期存在
    ftp.rename(file,"") #将文件移动至备份文件夹

# 本地文件备份
def bakupLocalFile(l):
    fileName = os.path.basename(l);
    bakFile = os.path.join(LOCAL_BAKFOLDER,fileName);
    print '%s,%s' %(l,bakFile)
    #shutil.copy2(fileName, bakFile)
    
def init():
    d =  time.strftime('%Y%m%d')
    if LOCAL_BAKFOLDER =='':
        LOCAL_BAKFOLDER = os.getcwd();
    bakFolder = os.path.join(LOCAL_BAKFOLDER,d);
    #备份文件夹是否存在
    if not os.path.exists(bakFolder):
        os.mkdir(bakFolder);

#准备Ftp环境,连接FTP服务器
def initFtp(server):
    ftp = FTP(server['ip']);
    ftp.login(server['username'], server['password'])
    return ftp

#记取配置文件,将要操作的数据方到一个list中
def initConf():
     confFile = open(os.path.join(os.getcwd(),UPDATE_FILE))
     lines = confFile.readlines()
     return lines;
  
if __name__ == '__main__':
    init();
    lines = initConf(); #读取更新文件列表
    for server in servers:
        if server['type']=='LOCAL':
            for line in lines:
                bakupLocalFile(line)

        
