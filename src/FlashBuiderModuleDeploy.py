#-*- coding: UTF-8 -*
'''
Created on 2011-10-31
 Flash Builder Module部署,将所有的模块添加至.actionScriptProperties
@author: Administrator
'''

import os
import xml.etree.ElementTree as ET


MODULE_DIR=r'F:\SuiXingPay\Repos\随行付_收单\src\ubui\src\modules'
PROPERTIES_FILE=r'F:\SuiXingPay\Repos\随行付_收单\src\ubui\.actionScriptProperties'
tree='' #xml root
def walkMoulde(modules,dir):
    dir = dir.decode('utf8').encode('gbk')
    for root,dirs,files in os.walk(dir):
        for file in files:
            #print os.path.join(root,file)
            if file.endswith('Module.mxml') :
                dealModule(modules,root,file);            

    
def dealModule(modules,root,file):
    path =  root[root.find('modules'):]
    path = path.replace('\\','/')
    destPath = path+'/'+file.replace('mxml','swf')
    sourcePath = path+'/'+file
    print '%s %s ' %(destPath,sourcePath)
    m = ET.SubElement(modules,"module")
    m.set('application',r'src/index.mxml')
    m.set('destPath',destPath)
    m.set('optimize','true')
    m.set('sourcePath',sourcePath)

def parseXML(xmldoc):
    global tree
    docPath = xmldoc.decode('utf8').encode('gbk')
    tree = ET.parse(docPath)
    modules =tree.find('modules')
    modules.clear()
    return modules

if __name__ == '__main__':
    modulesNode = parseXML(PROPERTIES_FILE)
    walkMoulde(modulesNode,MODULE_DIR)
    tree.write(PROPERTIES_FILE.decode('utf8').encode('gbk'))
    
