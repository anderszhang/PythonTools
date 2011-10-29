#! /usr/bin/python
#-*- coding: UTF-8 -*-

import sys
import os
from xml.dom import minidom

macroNodes =''

#写接口XML
def main(xmlFile,txcode):
	domImpl = minidom.getDOMImplementation()
	
	xmldoc = minidom.parse(xmlFile)
	transNodes = xmldoc.getElementsByTagName('Transaction')
	global macroNodes
	macroNodes = xmldoc.getElementsByTagName('Macro')
	for transNode in transNodes:
		if txcode != '':
			if transNode.attributes["code"].value== txcode:
				createFile(domImpl,transNode)
		else:
			createFile(domImpl,transNode)
#生成配置文件
def createFile(domImpl,transNode):
	doc = domImpl.createDocument(None,'body',None)
	body = doc.documentElement;

	txcode = transNode.attributes['code'].value
	#if txcode[0:2]== '46':
	#	filename = '040'+txcode[2:]+'_d.xml'
	#else:
	filename = txcode+'_d.xml'	
	print 'deal transaction '+txcode+'>'+filename
	reqNode = transNode.getElementsByTagName('Request')[0]
	itemNodes = reqNode.childNodes;
	#itemNodes = reqNode.getElementsByTagName('Item') 
	#循环接口文件中的item
	for itemNode in itemNodes:
                if itemNode.nodeType != itemNode.ELEMENT_NODE:
                        continue 
		if itemNode.nodeName =='Item':
			createItem(doc,body,itemNode)
		elif itemNode.nodeName =='Quote':
			macroName = itemNode.attributes['name'].value
			dealMacro(doc,macroName,body)
	if os.path.exists(os.getcwd()+'//interface')==False:
		os.mkdir('interface')
	interFile = open('interface//'+filename,'w')
	interFile.write(doc.toprettyxml())
	interFile.close()

#处理宏节点
def dealMacro(doc,macroName,body):
	for macroNode in macroNodes:
		if macroNode.attributes['name'].value == macroName:
			for itemNode  in  macroNode.getElementsByTagName('Item'):
				if itemNode.nodeName == 'Item':
					createItem(doc,body,itemNode)

#生成节点文件
def createItem(doc,body,itemNode):
	field = doc.createElement('field')
	name = itemNode.attributes['name'].value
        field.setAttribute('name',name)
        #如果为金额,使用数据字典
        if name.endswith('Amt')==True or name.endswith('Fee')==True:
                field.setAttribute('dictItem','AMT') 
        elif itemNode.hasAttribute('length')==True:
                field.setAttribute('length',itemNode.attributes['length'].value)
                       
	body.appendChild(field)

#主程序
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
 
