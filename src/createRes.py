#! /usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import os
from xml.dom import minidom



#写接口XML
def main(xmlFile,txcode):
        #解析minidom打开GBK编码的问题
	domImpl = minidom.getDOMImplementation()
	#data = open(xmlFile);
	#data = data.replace('GBK','utf8')
	xmldoc = minidom.parse(xmlFile)
	#xmldoc = minidom.parseString(data)
	global macroNodes
	macroNodes = xmldoc.getElementsByTagName('Macro')
	transNodes = xmldoc.getElementsByTagName('Transaction')
	for transNode in transNodes:
		if txcode != '':
			if transNode.attributes["code"].value== txcode:
				createFile(domImpl,transNode)
		else:
			createFile(domImpl,transNode)
#生成解包接口文件
def createFile(domImpl,transNode):
	doc = domImpl.createDocument(None,'body',None)
	body = doc.documentElement;
	txcode =transNode.attributes['code'].value
	sys.stdout.write('deal transaction '+txcode +">>>>>>>>>")
	#fileName =createFileName(txcode)
	fileName=''
	resNodes= transNode.getElementsByTagName('Response')
	if len(resNodes) == 0:
		return 0;
	resNode = resNodes[0]
        caseNodes = resNode.getElementsByTagName('Case')
        #如果存在Case节点,取Case节点,否则取If
        if len(caseNodes) >0:
                PNode = caseNodes[0]
        else:
                ifNodes = resNode.getElementsByTagName('If')
                PNode=ifNodes[0]
	#循环接口文件中的item
	#for caseNode in caseNodes:
	#	if caseNode.attributes['value'].value=='N':
	#		pkgNodes= caseNode.getElementsByTagName('PackItem')

        pkgNodes =  PNode.getElementsByTagName('PackItem')
        if len(pkgNodes)==0:
                print 'billText,no interface file'
                return 0
        pkgNode = pkgNodes[0]
        #itemNodes = pkgNode.getElementsByTagName('Item')
        itemNodes = pkgNode.childNodes
        filename = createFileName(itemNodes)

        #根据是否存在Group节点,看是否为列表交易
        groupNodes = pkgNode.getElementsByTagName('Group')
        if len(groupNodes)>0 :
                #找到Group节点,为列表交易
                groupNode = groupNodes[0]
                pkgNodes = groupNode.getElementsByTagName('PackItem')
                pkgNode = pkgNodes[0]
                itemNodes = pkgNode.getElementsByTagName('Item')            
                #itemNodes = pkgNode.childNodes;
                createInterfaceFile(filename,itemNodes,doc,body,True)
        else:
                createInterfaceFile(filename,itemNodes,doc,body,False)
        print filename+' finish'

                

#生成新的接口文件
def createInterfaceFile(filename,itemNodes,doc,body,listFlag):
        #列表交易,生成block
        if listFlag==True:
                block = doc.createElement('block')
                block.setAttribute('name','L')
                block.setAttribute('type','table')
        for itemNode in itemNodes:
                if itemNode.nodeType != itemNode.ELEMENT_NODE :
                        continue 
                if itemNode.nodeName =='Quote':
                        name = itemNode.attributes['name'].value
			dealMacro(name,body,doc)
                elif itemNode.nodeName =='Item':
                        name = itemNode.attributes['name'].value
                        if name =='ApCode' or name =='OFmtCd':
                                pass
                        else:
                                #列表
                                if listFlag == True:
                                        block = createFieldNode(itemNode,block,doc);
                                        body.appendChild(block)
                                else:
                                        createFieldNode(itemNode,body,doc);
        if os.path.exists(os.getcwd()+'//interface')==False:
                os.mkdir('interface') 
        interFile = open('interface//'+filename,'w')
        interFile.write(doc.toprettyxml())
        interFile.close()
        
#生成新的接口文件名
def createFileName(itemNodes):
        filename = ''
        for itemNode in itemNodes:
                if itemNode.nodeType == itemNode.ELEMENT_NODE and itemNode.nodeName=='Item':
                        if itemNode.attributes['name'].value =='ApCode' or itemNode.attributes['name'].value=='OFmtCd':
                                filename += itemNode.attributes['value'].value
        filename += '_d.xml'
	return filename
#处理
def dealMacro(macroName,pNode,doc):
	for macroNode in macroNodes:
		if macroNode.attributes['name'].value == macroName:
                        itemNodes = macroNode.getElementsByTagName('Item')
                        for itemNode in itemNodes:
                             createFieldNode(itemNode,pNode,doc)   
                        
#生成field节点
def createFieldNode(itemNode,pNode,doc):
        name = itemNode.attributes['name'].value
        field = doc.createElement('field')
        field.setAttribute('name',name)
        #如果为金额,使用数据字典
        if name.endswith('Amt')==True or name.endswith('Fee')==True:
                field.setAttribute('dictItem','AMT') 
        elif itemNode.hasAttribute('length')==True:
                field.setAttribute('length',itemNode.attributes['length'].value)
        elif itemNode.hasAttribute('value') == True:
                field.setAttribute('length',str(len(itemNode.attributes['value'].value)))
        pNode.appendChild(field)
        return pNode
                
					
if __name__ == '__main__':
	anum = len(sys.argv)
	txcode = ''
	if anum<2:
		print 'use method: commond filename txcod'
		exit(0)
	if anum == 2:
		xmlFile=sys.argv[1]
	if anum == 3:
		xmlFile=sys.argv[1]
		txcode=sys.argv[2]
	print xmlFile,txcode
	main(xmlFile,txcode)
	
	 
