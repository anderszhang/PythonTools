# -*- coding: utf-8 -*-
'''
Created on 2011-10-28

@author: Administrator
'''
import os
import sys

def cdWalk(cdrom,cdcfile):
    export ='\n'
    #type = sys.getfilesystemencoding()
    for root,dirs,files in os.walk(cdrom):
 
        for d in dirs:
            export+="-d "+root+str(d).decode('gbk').encode('gbk')+'\n'
        for file in files:
            export+='-f ' +root+str(file).decode('gbk').encode('gbk')+'\n'       
        #print myname.decode('UTF-8').encode(type)
        export +="+"*70
        open(cdcfile,'w').write(export)
        
cdWalk('E:\Test', 'test.txt')
#if sys.argv[1] =='-e':
#    
#    print "读取目录文件写致test.txt"
#else:
#    print '使用方式'
