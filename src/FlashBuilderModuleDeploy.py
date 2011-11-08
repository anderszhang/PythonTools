#-*- coding: UTF-8 -*
'''
Created on 2011-10-31
 Flash Builder Module部署,将所有的模块添加至.actionScriptProperties
@author: Administrator
'''

import os
import xml.etree.ElementTree as ET
import ConfigParser
from xml.dom import minidom

#Module目录
MODULE_DIR=""
#.actionScriptProperties.xml
PROPERTIES_FILE=""
tree='' #xml root

#遍历modules目录,查询根结点为Module的文件
def walkMoulde(modules,dir):
    #遍历文件夹
    for root,dirs,files in os.walk(dir):
        for file in files:
            filepath = os.path.join(root,file)
            if file.endswith('.mxml'):
                tmpFile = ET.parse(filepath)
                tmpRoot = tmpFile.getroot();
                tag = tmpRoot.tag
                if(tag.endswith('Module')): #如果根结点为Module
                    dealModule(modules,root,file);            

#给modules节点增加新的节点    
def dealModule(modules,root,file):
    path =  root[root.find('modules'):]
    path = path.replace('\\','/')
    destPath = path+'/'+file.replace('mxml','swf')
    sourcePath = 'src'+'/'+path+'/'+file
    print '%s %s ' %(destPath,sourcePath)
    m = ET.SubElement(modules,"module")
    m.set('application',r'src/index.mxml')
    m.set('destPath',destPath)
    m.set('optimize','true')
    m.set('sourcePath',sourcePath)
    #print ET.tostring(m)
    
#解析.actionProperties.xml文件,返回modules节点    
def parseXML(xmldoc):
    global tree
    tree = ET.parse(xmldoc)
    modules =tree.find('modules')
    modules.clear()
    return modules

#读取FlashBuilderModuleDeploy.cfg配置文件
def init():
    global MODULE_DIR,PROPERTIES_FILE
    cfg = ConfigParser.RawConfigParser()
    cfg.read('FlashBuilderModuleDeploy.cfg')
    MODULE_DIR = cfg.get('Deploy', 'MODULE_DIR').replace("'","")
    PROPERTIES_FILE = cfg.get('Deploy', 'PROPERTIES_FILE').replace("'","")
    
#main函数,程序入口
if __name__ == '__main__':
    init();
    modulesNode = parseXML(PROPERTIES_FILE)
    walkMoulde(modulesNode,MODULE_DIR)
    tree.write(PROPERTIES_FILE)
    #以上为用minidom格式化xml
   # reparsed = minidom.parseString(ET.tostring(tree.getroot()))  
    #print reparsed.toprettyxml(indent="  " , encoding="utf-8");  
    
