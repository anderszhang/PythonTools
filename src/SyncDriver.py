#-*- coding: UTF-8 -*
'''
Created on 2011-9-29
 自动与U盘同步文件
@author: anderszhang
email:anderszhang@gmail.com
'''

import os
import locale
import shutil

DRIVER_PATH='F:\\'
COMPUTER_PATH=''
CHARSET=''
copyNum=0

#根据操作系统初始化路径
def initPath():
    '''
        根据操作系统初始过路径
    '''
    global COMPUTER_PATH
    global CHARSET
    CHARSET = locale.getdefaultlocale()[1];
    if os.name == 'nt': 
        COMPUTER_PATH =r"E:\Book\CSS"
    elif os.name == 'posix':
        COMPUTER_PATH=''
        
#遍历文件夹    
def walk(srcPath,targetPath):
    l = len(srcPath)
    for root,dirs,files in os.walk(srcPath): #遍历源的所有文件
        for f in files:
            srcFilePath = os.path.join(root,f)
            targetFilePath = os.path.join(targetPath,root[l:],f) #拼接目标文件路径
            if not os.path.exists(targetFilePath):
                copyFile(srcFilePath, targetFilePath)
            else:
                sMtime = os.stat(srcFilePath).st_mtime 
                tMtime = os.stat(srcFilePath).st_mtime
                if(sMtime>tMtime): #比较两个文件的最后修改时间
                    copyFile(srcFilePath, targetFilePath)
                elif(sMtime<tMtime):
                    copyFile(targetFilePath,srcFilePath)


#复制文件
def copyFile(srcFile,targetFile):
    global copyNum
    path = os.path.dirname(targetFile)
    if not os.path.exists(path):
        os.mkdir(path)
    shutil.copy2(srcFile, targetFile)
    #print unicode(srcFile,CHARSET)
    print '复制文件%s>>>>>>>>>>>>>>>>>>>%s' %(unicode(srcFile,CHARSET),unicode(targetFile,CHARSET));
    copyNum = copyNum+1;
    
if __name__ == '__main__':
    initPath()
    walk(COMPUTER_PATH,DRIVER_PATH) #正向检查
    walk(DRIVER_PATH,COMPUTER_PATH) #反向检查
    print '同步完成,同计同步文件%d 个' %(copyNum)
