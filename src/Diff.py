#-*- coding: UTF-8 -*
'''
Created on 2011-9-29
 比较同名但大小不同的文件
@author: anderszhang
email:anderszhang@gmail.com
'''

import os

TAR_PATH='F:\Workspace\Helios\Branch\WebRoot\WEB-INF\lib\\branch_sit\com\hisun\\branch'
SRC_PATH='F:\Code\\branch20110926\\branch\WEB-INF\classes\com\hisun\\branch'
#比较文件数目
copyNum=0


#遍历文件夹
def findDiffFile(srcPath,targetPath):
    global copyNum
    l = len(srcPath)+1
    for root,dirs,files in os.walk(srcPath):
        for f in files:
            srcFilePath = os.path.join(root,f)
            targetFilePath = os.path.join(targetPath,root[l:],f)
            srcSize = os.stat(srcFilePath).st_size
            if not os.path.exists(targetFilePath):
               # print '%s %s' %(srcFilePath,srcSize)
               #copyNum +=1
                pass
            else :
                tarSize = os.stat(targetFilePath).st_size
                if srcSize != tarSize:
                    print '%s %sK || %s %s' %(srcFilePath,srcSize,targetFilePath,tarSize)
                    copyNum +=1
                    
if __name__ == '__main__':
    findDiffFile(SRC_PATH,TAR_PATH)
    print '比较完成,同计不同文件%d个' %(copyNum)
