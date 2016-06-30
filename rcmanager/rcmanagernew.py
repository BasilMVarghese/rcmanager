#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  -----------------------
#  -----  rcmanager  -----
#  -----------------------
#  An ICE component manager.
#
#    Copyright (C) 2009-2015 by RoboLab - University of Extremadura
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#

#
# CODE BEGINS
#

import sys, time, traceback, os, math, random, threading, time
import Ice

from time import localtime, strftime##To log data
from PyQt4 import QtCore, QtGui, Qt
import rcmanagerUItemplate,rcmanagerConfignew

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class MainClass(QtGui.QMainWindow):
	"""docstring for MainClass"""
	def __init__(self, arg=None):
		QtGui.QDialog.__init__(self,arg)
		self.componentList=[]
		self.networkSettings=rcmanagerConfignew.getDefaultValues()
		self.UI=rcmanagerUItemplate.Ui_MainWindow()
		self.UI.setupUi(self)
		self.NetworkScene=rcmanagerConfignew.ComponentScene()##The graphicsScene
		self.graphTree = rcmanagerConfignew.ComponentTree(self.UI.frame,self)##The graphicsNode
		self.graphTree.setScene(self.NetworkScene)
		self.graphTree.setObjectName(_fromUtf8("graphicsView"))
		self.UI.gridLayout_8.addWidget(self.graphTree,0,0,1,1)
		#self.node=rcmanagerConfignew.VisualNode(self.graphTree)
		#self.node.setIcon("share/rcmanager/DefaultIcon.png")
		#self.node.setIpColor()
		#self.NetworkScene.addItem(self.node)
		self.setZoom()
		self.setupActions()
	def setupActions(self):##To setUp connection like saving,opening,etc
		self.connect(self.UI.actionSave,QtCore.SIGNAL("triggered(bool)"),self.saveXmlFile)
		self.connect(self.UI.actionOpen,QtCore.SIGNAL("triggered(bool)"),self.openXmlFile)
		self.connect(self.UI.actionExit,QtCore.SIGNAL("triggered(bool)"),self.exitRcmanager)
		self.connect(self.UI.actionSetting,QtCore.SIGNAL("triggered(bool)"),self.rcmanagerSetting)
		self.connect(self.UI.actionON,QtCore.SIGNAL("triggered(bool)"),self.simulatorOn)
		self.connect(self.UI.actionOFF,QtCore.SIGNAL("triggered(bool)"),self.simulatorOff)
		self.connect(self.UI.actionSetting_2,QtCore.SIGNAL("triggered(bool)"),self.simulatorSettings)
		self.connect(self.UI.actionSetting_3,QtCore.SIGNAL("triggered(bool)"),self.controlPanelSettings)
		self.connect(self.UI.actionSetting_4,QtCore.SIGNAL("triggered(bool)"),self.editorSettings)
		self.connect(self.graphTree.BackPopUpMenu.ActionUp,QtCore.SIGNAL("triggered(bool)"),self.upAllComponents)
		self.connect(self.graphTree.BackPopUpMenu.ActionDown,QtCore.SIGNAL("triggered(bool)"),self.downAllComponents)
		self.connect(self.graphTree.BackPopUpMenu.ActionSearch,QtCore.SIGNAL("triggered(bool)"),self.searchInsideTree)
		self.connect(self.graphTree.BackPopUpMenu.ActionAdd,QtCore.SIGNAL("triggered(bool)"),self.addNode)		
		self.connect(self.graphTree.BackPopUpMenu.ActionSettings,QtCore.SIGNAL("triggered(bool)"),self.setNetworkSettings)
		self.connect(self.graphTree.CompoPopUpMenu.ActionUp,QtCore.SIGNAL("triggered(bool)"),self.upSelectedComponent)
		self.connect(self.graphTree.CompoPopUpMenu.ActionDown,QtCore.SIGNAL("triggered(bool)"),self.downComponent)
		#self.connect(self.graphTree.CompoPopUpMenu.ActionNewConnection,QtCore.SIGNAL("triggered(bool)"),self.upComponent)
		self.connect(self.graphTree.CompoPopUpMenu.ActionControl,QtCore.SIGNAL("triggered(bool)"),self.controlComponent)
		self.connect(self.graphTree.CompoPopUpMenu.ActionSettings,QtCore.SIGNAL("triggered(bool)"),self.componentSettings)
		self.logToDisplay("Tool Started")
	def ipclassify(self):#To find all the computer present
		self.ipList=[]##Ip listed from the xml file
		for x in self.componentList.__iter__():
			flag=False
			for y in ipList.__iter__():
				if y==x.Ip:
					flag=True
					break
			if flag==False:
				ipList.append(x.Ip)
	def setAllIpColor(self):
		diff=int(655/self.ipList().__le__())

				
	def logToDisplay(self,text=" ",color=QtGui.QColor.fromRgb(24,149,99)):#To log into the textEdit widget
		time=strftime("%Y-%m-%d %H:%M:%S", localtime())
		self.UI.textBrowser.setTextColor(color)
		self.UI.textBrowser.append(time +"  >>  "+ text)
	def componentSettings(self,component):#To edit the settings of currentComponent
		print "Settings of current component"
	def controlComponent(self,component):#To open up the control panel of current component
		print "Controlling the current component"	
	def downComponent(self,component):#To down a particular component
		print "Downing particular component"
	def upComponent(self,component):#Just Up the component
		try:
			proc=QtCore.QProcess()
			proc.startDetached(component.parent.compup)
			self.logToDisplay(component.parent.alias+" ::started")
		except Exception, e:
			self.logToDisplay("Cannot write"+str(e))
			raise e
		else:
			pass
		finally:
			pass

	def upSelectedComponent(self):#This will up a selected component
		component=self.graphTree.CompoPopUpMenu.currentComponent
		self.upComponent(component)
	def setNetworkSettings(self):#To edit the network tree general settings
		print "network setting editing"	
	def searchInsideTree(self):#To search a particular component from tree
		print "Searching inside the tree"
	def upAllComponents(self):#To set all components in up position
		print "UPING ALL"
	def downAllComponents(self):#To set all components in down position
		print "Down All"
	def drawfromfile(self,nodelist):#To be called when a new tree have to be drawn which was directly read from file
		pass
	def simulatorSettings(self):##To edit the simulatorSettings:Unfinished
		print "Simulator settings is on"
	def controlPanelSettings(self):##To edit the controlPanel Settings:Unfinshed
		print "Control panel settings"
	def editorSettings(self):##To edit the editors settins:Unfinshed
		print "Editor Settings"	
	def simulatorOff(self):	#To switch Off the simulator::Unfiunished
		print "Simulator is Off"
	def simulatorOn(self):#To switch ON simulator::Unfinished
		print "Simulator is On"
	def rcmanagerSetting(self):#To edit the setting of the entire rcmanager settings tool
		print "Opened tool settings"	
	def exitRcmanager(self):##To exit the tool after doing all required process
		print "Exiting"
	def drawComponents(self):#Called to draw the components
		for x in self.componentList.__iter__():
			self.NetworkScene.addItem(x.graphicsItem)
	def openXmlFile(self):#To open the xml files ::Unfinished
		try:	
			self.filePath=QtGui.QFileDialog.getOpenFileName(self,'Open file',os.getcwd(),'*.xml')
			self.componentList , self.networkSettings=rcmanagerConfignew.getConfigFromFile(self.filePath)
			self.drawComponents() 
			self.logToDisplay("File "+self.filePath +"  Read successfully")
		except:
			self.logToDisplay("Opening File Failed",QtGui.QColor.fromRgb(255,0,0))
	def saveXmlFile(self):##To save the entire treesetting into a xml file::Unfinished
		try:
			saveFileName=QtGui.QFileDialog.getSaveFileName(self,'Save File','/home/h20','*.xml')
			rcmanagerConfignew.writeConfigToFile(self.networkSettings,self.componentList,saveFileName)
			self.logToDisplay("Saved to File "+saveFileName+" ::SuccessFull")
		except:
			self.logToDisplay("Saving to File"+saveFileName+" ::Failed",QtGui.QColor.fromRgb(255,0,0))
	def setZoom(self): ##To connect the slider motion to zooming
		self.UI.verticalSlider.setRange(-20,20)
		self.UI.verticalSlider.setTickInterval(1)
		self.UI.verticalSlider.setValue(0)
		self.currentZoom=0
		self.UI.verticalSlider.valueChanged.connect(self.graphZoom)
	def graphZoom(self):##To be called when ever we wants to zoomingfactor
		new=self.UI.verticalSlider.value()
		diff=new-self.currentZoom
		self.currentZoom=new
		zoomingfactor=math.pow(1.2,diff)
		#print zoomingfactor
		self.graphTree.scale(zoomingfactor,zoomingfactor)
	def addNode(self):#For adding a new node in the network
		pass
	def addComponent(self):#adding new component on the right component list
		pass
	

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window=MainClass()
	window.show()
	try:
		ret = app.exec_()
	except:
		print 'Some error happened.'

	sys.exit()
