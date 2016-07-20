#!/usr/bin/env python2.7
#
#  -----------------------
#  ----- rcmanager -----
#  -----------------------
#  An ICE component manager.
#

#    Copyright (C) 2008-2010 by RoboLab - University of Extremadura
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
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#


# Importamos el modulo libxml2
import libxml2, sys,threading,Ice ,time,os 
import SaveWarning,toolsettingsUI
from PyQt4 import QtCore, QtGui, Qt,Qsci
filePath = 'rcmanager.xml'


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class toolSettings(QtGui.QDialog):#This will show a dialog window for selecting the rcmanager tool settings
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self)
		self.parent=parent
		self.UI=toolsettingsUI.Ui_Dialog()			
		self.UI.setupUi(self)
		self.fontsettingsWorkspace=QtGui.QWorkspace(self.UI.tab_2)
		self.fontDialog=QtGui.QFontDialog(self.fontsettingsWorkspace)
		self.fontsettingsWorkspace.addWindow(self.fontDialog)

class SaveWarningDialog(QtGui.QDialog):#To be used as a warning window while deleting existing tree without saving
	def __init__(self,parent=None):
		QtGui.QDialog.__init__(self)
		self.parent=parent
		self.UI=SaveWarning.Ui_Dialog()
		self.UI.setupUi(self)
		self.connect(self.UI.pushButton_2,QtCore.SIGNAL("clicked()"),self.save)
		self.connect(self.UI.pushButton,QtCore.SIGNAL("clicked()"),self.dontSave)
		self.connect(self.UI.pushButton_3,QtCore.SIGNAL("clicked()"),self.cancel)
		self.setModal(True)
		self.Status="C"
	def decide(self):
		self.exec_()
		return self.Status
	def save(self):
		self.close()
		self.Status="S"
	def dontSave(self):
		self.close()
		self.Status="D"
	def cancel(self):
		self.close()
		self.Status="C"

class CodeEditor(Qsci.QsciScintilla):#For the dynamic code editing (Widget )
	def __init__(self,parent=None):
		Qsci.QsciScintilla.__init__(self,parent)

		#Setting default font
		self.font=QtGui.QFont()
		self.font.setFamily('Courier')
		self.font.setFixedPitch(True)
		self.font.setPointSize(10)
		self.setFont(self.font)
		self.setMarginsFont(self.font)


		# Margin 0 is used for line numbers
		fontmetrics =QtGui.QFontMetrics(self.font)
		self.setMarginsFont(self.font)
		self.setMarginWidth(0,fontmetrics.width("0000") + 6)
		self.setMarginLineNumbers(0, True)
		self.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))		

		#BraceMatching
		self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)

		# Current line visible with special background color
		self.setCaretLineVisible(True)
		self.setCaretLineBackgroundColor(QtGui.QColor("#ffe4e4"))

		#Setting xml lexer
		lexer = Qsci.QsciLexerXML()
		lexer.setDefaultFont(self.font)
		self.setLexer(lexer)
		self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
	
	def on_margin_clicked(self, nmargin, nline, modifiers):
		# Toggle marker for the line the margin was clicked on
		if self.markersAtLine(nline) != 0:
			self.markerDelete(nline, self.ARROW_MARKER_NUM)
		else:
			self.markerAdd(nline, self.ARROW_MARKER_NUM)

class VisualNode(QtGui.QGraphicsItem):##Visual Node GraphicsItem
	"""docstring for ClassName"""
	def __init__(self, view=None,Alias=None,parent=None):
		QtGui.QGraphicsItem.__init__(self)
		self.parent=parent
		self.view=view
		self.Alias=Alias
		self.pos=None
		self.IpColor=None
		self.aliveStatus=False
		self.detailsShower=None
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
		self.setAcceptHoverEvents(True)
		#self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
		self.setZValue(1)#To make sure the Nodes are always on top of connections
	def mouseMoveEvent(self,event):
		self.parent.mainWindow.nodeDetailDisplayer.hide()
		QtGui.QGraphicsItem.mouseMoveEvent(self,event)
		self.updateforDrag()
		self.parent.emit(QtCore.SIGNAL("networkChanged()"))
		#print "Changed"

	def updateforDrag(self):
		for x in self.parent.asBeg.__iter__():
			end=x.toComponent
			a,b=findWhichPorts(self.parent,end)
			x.fromX,x.fromY=findPortPosition(self.parent,a)
			x.toX,x.toY=findPortPosition(end,b)
			x.prepareGeometryChange()
		for x in self.parent.asEnd.__iter__():
			beg=x.fromComponent
			a,b=findWhichPorts(beg,self.parent)
			x.fromX,x.fromY=findPortPosition(beg,a)
			x.toX,x.toY=findPortPosition(self.parent,b)
			x.prepareGeometryChange()
		self.scene().update()
	def mouseReleaseEvent(self,event):
		QtGui.QGraphicsItem.mouseReleaseEvent(self,event)
		self.updateforDrag(	)
	def hoverEnterEvent(self,event):
		#print self.parent.mainWindow.graphTree
		pos=self.parent.mainWindow.graphTree.mapFromScene(self.mapToScene(QtCore.QPointF()))
		self.parent.mainWindow.nodeDetailDisplayer.showdetails(pos.x(),pos.y(),self.parent)
	def hoverLeaveEvent(self,event):
		self.parent.mainWindow.nodeDetailDisplayer.isShowing=False
		self.parent.mainWindow.nodeDetailDisplayer.hide()

	def setIpColor(self,color=QtGui.QColor.fromRgb(0,255,0)):#To set the Ipcolor
		self.IpColor=color
	def setview(view):
		self.view=view
	def boundingRect(self):
		self.penWidth =2
		return QtCore.QRectF(-69,-69,138,138)
	def paint(self,painter,option=None,widget=None):
		self.paintMainShape(painter)
		self.drawStatus(painter)
		self.drawIcon(painter)
		self.writeAlias(painter)
	def setIcon(self,icon):
		self.Icon=icon
	def paintMainShape(self,painter): ##This will draw the basic shape of a node.The big square and its containing elements
		pen=QtGui.QPen(QtGui.QColor.fromRgb(0,0,0))
		pen.setWidth(3)
		painter.setPen(pen)
		brush=QtGui.QBrush(QtGui.QColor.fromRgb(94,94,94))
		painter.setBrush(brush)
		painter.drawRoundedRect(-49,-49,98,98,5,5)
		
		self.TextRect=QtCore.QRect(-45,-45,90,20)##The rectangle shape on which the alias name will be dispalyed
		self.statusRect=QtCore.QRect(22,10,20,20)##The rectange shape on which the status of the node will be displayed
		self.IconRect=QtCore.QRect(-45,-20,60,64)## The rectange shape on which the Icon will be displayed
		
		
		brush.setColor(QtGui.QColor.fromRgb(94,94,94))
		self.drawUpPort(painter,brush)##Temp
		self.drawDownPort(painter,brush)##Temp
		self.drawRightPort(painter,brush)##Temp
		self.drawLeftPort(painter,brush)##Temp
		
		brush.setColor(QtGui.QColor.fromRgb(255,255,255))
		painter.setBrush(brush)
		painter.drawRect(self.TextRect) ##Drawing the Alias display rectangle
		painter.setBrush(self.IpColor)  ## Drawing the Icon display rectangle
		painter.drawRect(self.IconRect)
		
		
	def drawUpPort(self,painter,brush):##The bulging arcs will can be calleds as the port because all connection starts from there
		painter.setBrush(brush)
		painter.drawChord(-10,-59,20,20,0,2880)
	
	def drawDownPort(self,painter,brush):
		painter.setBrush(brush)
		painter.drawChord(-10,39,20,20,0,-2880)

	def drawRightPort(self,painter,brush):
		painter.setBrush(brush)
		painter.drawChord(39,-10,20,20,1440,-2880)

	def drawLeftPort(self,painter,brush):
		painter.setBrush(brush)
		painter.drawChord(-59,-10,20,20,1440,2880)

	def drawIcon(self,painter):#Draw the Icon representing the purpose and draw its 
		painter.setBrush(self.IpColor)  ## Drawing the Icon display rectangle
		painter.drawRect(self.IconRect)
		painter.drawPixmap(-45,-20,60,60,self.Icon,0,0,0,0)
	def writeAlias(self,painter):##Draw the alias
		painter.drawText(self.TextRect,1," "+self.Alias) 	##Drawing the Alias name
	def drawStatus(self,painter):
		if self.parent.status:
			brush=QtGui.QBrush(QtGui.QColor.fromRgb(0,255,0)) ##Drawing the Status display rectangle
			painter.setBrush(brush)
			painter.drawRect(self.statusRect)
		else:
			brush=QtGui.QBrush(QtGui.QColor.fromRgb(255,0,0)) ##Drawing the Status display rectangle
			painter.setBrush(brush)
			painter.drawRect(self.statusRect)

def findPortPosition(Component,Port):#PORT can be "U"or "D" or "R" or "L"
		ItemPoint=QtCore.QPointF()
		if Port=="U":
			ItemPoint.setX(0)
			ItemPoint.setY(-54)
			X=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).x()
			Y=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).y()
			return X,Y
		elif Port=="D":
			ItemPoint.setX(0)
			ItemPoint.setY(54)
			X=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).x()
			Y=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).y()
			return X,Y
		elif Port=="R":
			ItemPoint.setX(54)
			ItemPoint.setY(0)
			X=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).x()
			Y=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).y()
			return X,Y	
		elif Port=="L":
			ItemPoint.setX(-54)
			ItemPoint.setY(0)
			X=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).x()
			Y=QtGui.QGraphicsItem.mapToScene(Component.graphicsItem,ItemPoint).y()
			return X,Y


def findWhichPorts(fromComponent,toComponent):#This will select out of the 4 ports which have to be connected to connection		
		
		a=fromComponent.graphicsItem.mapToScene(QtCore.QPointF())
		b=toComponent.graphicsItem.mapToScene(QtCore.QPointF())

		Line=QtCore.QLineF(b,a)
		
		angle=Line.angle()
		#print angle
		if angle<=45 or angle >315:
			return "L","R"
		elif angle>45 and angle<=135:
			return "D","U"
		elif angle>135 and angle <=225:
			return "R","L"
		elif angle>225 and angle <=315:
			return "U","D"

class NodeConnection(QtGui.QGraphicsItem):
	def __init__(self):
		QtGui.QGraphicsItem.__init__(self)
		self.fromComponent=None
		self.toComponent=None
		self.fromX=0
		self.fromY=0
		self.toX=0
		self.toY=0
		self.color=QtGui.QColor.fromRgb(0,255,0)
		self.pen=QtGui.QPen(self.color)
		self.penWidth=2
		self.pen.setWidth(self.penWidth)
		self.setBoundingRegionGranularity(0.9)
		self.Line=None
		self.fromPoint=QtCore.QPointF()
		self.toPoint=QtCore.QPointF()	
	def boundingRect(self):##TO Be modified..Because error prone when vertical and horizontal
		if abs(self.toX-self.fromX)<5:
			width=5
		else:
			width=self.toX-self.fromX
		if abs(self.toY-self.fromY)<5:
			height=5
		else:
			height=self.toY-self.fromY
		self.rect=QtCore.QRectF(self.fromX,self.fromY,width,height)
		return self.rect
	def paint(self,painter,option=None,widget=None):
		painter.setPen(self.pen)
		self.fromPoint.setX(self.fromX)
		self.fromPoint.setY(self.fromY)
		self.toPoint.setX(self.toX)
		self.toPoint.setY(self.toY)
		self.Line=QtCore.QLineF(self.fromPoint,self.toPoint)
		painter.drawLine(self.Line)
		#painter.drawRect(self.rect)
	def drawarrows(self,painter):#To draw the arrows in the connections::Unfinished
		cener=(self.fromPoint+self.toPoint)/2
#	self.Line
				
class ComponentChecker(threading.Thread):#This will check the status of components
	def __init__(self):
		threading.Thread.__init__(self)
		self.component=None
		self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
		self.daemon = True
		self.reset()
		self.exit = False
		self.alive = False
		self.aPrx = None
	def initializeComponent(self,component):#Called to set the component and to initialize the Ice proxy
		self.component=component
		try:
			ic=Ice.initialize(sys.argv)
			self.aPrx = ic.stringToProxy(self.component.endpoint)
			self.aPrx.ice_timeout(1)
		except:
			print "Error creating proxy to " + self.component.endpoint
			if len(self.component.endpoint) == 0:
				print 'please, provide an endpoint'
			raise

	def run(self):
		global global_ic
		while self.exit == False:
			try:
				self.aPrx.ice_ping()
				self.mutex.lock()
				if self.alive==False:
					self.changed()	
				self.alive = True
				self.mutex.unlock()
			except:
				self.mutex.lock()
				if self.alive==True:
					self.changed()
				self.alive = False
				self.mutex.unlock()
			#self.mutex.lock()
			#print self.component.alias +" ::Status:: "+ str(self.alive)
			#self.mutex.unlock()
			time.sleep(0.5)
	def reset(self):
		self.mutex.lock()
		self.alive = False
		self.mutex.unlock()
	def isalive(self):
		self.mutex.lock()
		r = self.alive
		self.mutex.unlock()
		return r
	def stop(self):
		self.exit = True
	def runrun(self):
		if not self.isAlive(): self.start()#Note this is different isalive
	def changed(self):
		self.component.status=not self.alive
		self.component.graphicsItem.update()

class ShowItemDetails(QtGui.QWidget):##This contains the GUI and internal process regarding the controlling of the a particular component.
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self)
		self.component=None
		self.setParent(parent)
		self.detailString=" "
		self.label=QtGui.QTextEdit(self)
		self.label.setGeometry(0,0,150,150)
		self.isShowing=False
		self.hide()
	def showdetails(self,x,y,item=None):
		self.label.setText(item.alias)
		self.setGeometry(x,y,150,150)
	  	self.isShowing=True
	  	self.show()
#		
# Component information container class.
#
class CompInfo(QtCore.QObject):##This contain the general Information about the Components which is read from the files and created
	def __init__(self):

		QtCore.QObject.__init__(self)
		self.View=None
		self.mainWindow=None
		self.asEnd=[]#This is the list of connection where the node act as the ending point
		self.asBeg=[]#This is the list of connection where the node act as the beginning point
		self.endpoint = ''
		self.workingdir = ''
		self.compup = ''
		self.compdown = ''
		self.alias = ''
		self.dependences = []
		self.configFile = ''
		self.x = 0##This is not reliable >>Have to fix the bug
		self.y = 0##This is not reliable >>Have to fix the bug
		self.Ip=""
		self.IconFilePath=""
		self.status=False
		self.CheckItem=ComponentChecker()
		self.graphicsItem=VisualNode(parent=self)
		self.DirectoryItem=DirectoryItem(parent=self)
		#self.Controller=ComponentController(parent=self)
	def __repr__(self):
		string = ''
		string = string + '[' + self.alias + ']:\n'
		string = string + 'endpoint:  \t' + self.endpoint + '\n'
		string = string + 'workingDir:\t' + self.workingdir + '\n'
		string = string + 'up:        \t' + self.compup + '\n'
		string = string + 'down:      \t' + self.compdown + '\n'
		string = string + 'x:         \t' + str(self.x) + '\n'
		string = string + 'y:         \t' + str(self.y) + '\n'
		string = string + 'Icon path: \t' + self.IconFilePath+"\n"
		return string	
	def setGraphicsData(self):#To set the graphicsItem datas
		self.graphicsItem.setIpColor()
		self.graphicsItem.setPos(self.x,self.y)
		self.graphicsItem.Alias=self.alias


class  ComponentTree(QtGui.QGraphicsView):	##The widget on which we are going to draw the graphtree 
	def __init__(self,parent,mainclass):
		self.viewportAnchor=QtGui.QGraphicsView.AnchorUnderMouse
		QtGui.QGraphicsView.__init__(self,parent)
		self.mainclass=mainclass#This object is the mainClass from rcmanager Module
		self.CompoPopUpMenu=ComponentMenu(self.mainclass)
		self.BackPopUpMenu=BackgroundMenu(self.mainclass)
	def wheelEvent(self,wheel):
		pos=self.mapToScene(wheel.pos())
		self.centerOn(pos)
		QtGui.QGraphicsView.wheelEvent(self,wheel)
		temp=self.mainclass.currentZoom
		temp+=(wheel.delta()/120)
		self.mainclass.UI.verticalSlider.setValue(temp)
		self.mainclass.graphZoom()
	def contextMenuEvent(self,event):##It will select what kind of context menu should be displayed
		GloPos=event.globalPos()
		pos=event.pos()
		item=self.itemAt(pos)
		#print pos#TEMP
		if isinstance(item,VisualNode):
			self.CompoPopUpMenu.setComponent(item)
			self.CompoPopUpMenu.popup(GloPos)
		else:
			self.BackPopUpMenu.pos=pos
			self.BackPopUpMenu.popup(GloPos)


class ComponentScene(QtGui.QGraphicsScene):#The scene onwhich we are drawing the graph
	def __init__(self,parent=None):
		QtGui.QGraphicsScene.__init__(self)
		self.parent=parent
	
class DirectoryItem(QtGui.QPushButton):#This will be listed on the right most side of the software

	def __init__(self,parent=None,args=None):
		QtGui.QPushButton.__init__(self,args)
		self.parent=parent
		self.args=args
	def setIcon(self,arg):
		self.Icon=QtGui.QIcon()
		self.Icon.addPixmap(arg)
		QtGui.QPushButton.setIcon(self,self.Icon)



class ComponentMenu(QtGui.QMenu):
	def  __init__(self,parent):

		QtGui.QMenu.__init__(self,parent)
		self.ActionUp=QtGui.QAction("Up",parent)
		self.ActionDown=QtGui.QAction("Down",parent)
		self.ActionSettings=QtGui.QAction("Settings",parent)
		self.ActionControl=QtGui.QAction("Control",parent)
		self.ActionNewConnection=QtGui.QAction("New Connection",parent)
		self.addAction(self.ActionUp)
		self.addAction(self.ActionDown)
		self.addAction(self.ActionNewConnection)
		self.addAction(self.ActionControl)
		self.addAction(self.ActionSettings)
	def setComponent(self,component):
		self.currentComponent=component




class BackgroundMenu(QtGui.QMenu):
	def __init__(self,parent):
		QtGui.QMenu.__init__(self,parent)
		self.ActionSettings=QtGui.QAction("Settings",parent)
		self.ActionUp=QtGui.QAction("Up All",parent)
		self.ActionDown=QtGui.QAction("Down All",parent)
		self.ActionSearch=QtGui.QAction("Search",parent)
		self.ActionAdd=QtGui.QAction("Add",parent)
		self.addAction(self.ActionUp)
		self.addAction(self.ActionDown)
		self.addAction(self.ActionSettings)
		self.addAction(self.ActionAdd)
		self.addAction(self.ActionSearch)
		self.pos=None
def getDefaultValues():
	dict = {}
	return dict

def getStringFromFile(path):##This is the first function to be called for reading configurations for a xml file
	try:
		file = open(path, 'r')
	except:
		print 'Can\'t open ' + path + '.'

	data = file.read()
	return data
def getDataFromString(data):#Data is a string in xml format containing information	
	components = []	
	xmldoc = libxml2.parseDoc(data)
	root = xmldoc.children
	
	if root is not None:
		components, NetworkSettings = parsercmanager(root)
	xmldoc.freeDoc()
	return components, NetworkSettings

def parsercmanager(node): #Call seperate functions for general settings and nodes
	components = []
	generalSettings=getDefaultValues()
	if node.type == "element" and node.name == "rcmanager":
		child = node.children
		while child is not None:
			if child.type == "element":
				if child.name == "generalInformation":
					parseGeneralInformation(child, generalSettings)
				elif child.name == "node":
					parseNode(child, components)
				elif stringIsUseful(str(node.properties)):
					print 'ERROR when parsing rcmanager: '+str(child.name)+': '+str(child.properties)
			child = child.next
	return components, generalSettings

def parseGeneralInformation(node, dict): ##Takes care of reading the general information about the network tree
	if node.type == "element" and node.name == "generalInformation":
		print "General Information read"

def parseGeneralValues(node, dict, arg):##Called to read the attribute values of elements of General Values
	if node.children != None: print 'WARNING: No children expected'
	for attr in arg:
		if node.hasProp(attr):
			dict[attr] = node.prop(attr)
			node.unsetProp(attr)

def checkForMoreProperties(node):
	if node.properties != None: print 'WARNING: Attributes unexpected: ' + str(node.properties)


def parseNode(node, components):#To get the properties of a component
	if node.type == "element" and node.name == "node":
		child = node.children
		comp = CompInfo()
		print "Started reading components"
		comp.alias = parseSingleValue(node, 'alias', False)
		comp.DirectoryItem.setText(comp.alias)
		comp.endpoint = parseSingleValue(node, 'endpoint', False)
		mandatory = 0
		block_optional = 0
		
		while child is not None:
			if child.type == "element":
				if child.name == "workingDir":
					comp.workingdir = parseSingleValue(child, 'path')
					mandatory = mandatory + 1
				elif child.name == "upCommand":
					comp.compup = parseSingleValue(child, 'command')
					mandatory = mandatory + 2
				elif child.name == "downCommand":
					comp.compdown = parseSingleValue(child, 'command')
					mandatory = mandatory + 4
				elif child.name == "configFile":
					comp.configFile = parseSingleValue(child, 'path')
					mandatory = mandatory + 8
				elif child.name == "xpos":
					x=parseSingleValue(child, 'value')
					comp.x = float(x)
					block_optional = block_optional + 1
				elif child.name == "ypos":
					comp.y = float(parseSingleValue(child, 'value'))
					block_optional = block_optional + 2
				elif child.name == "dependence":
					comp.dependences.append(parseSingleValue(child, 'alias'))
				elif child.name == "icon":
					parseIcon(child, comp)
				elif child.name == "ip":
					comp.Ip=parseSingleValue(child, "value")
				elif stringIsUseful(str(child.properties)):
					print 'ERROR when parsing rcmanager: '+str(child.name)+': '+str(child.properties)
			child = child.next
		if mandatory<15:
			if   mandatory^15 == 1: print 'ERROR Not all mandatory labels were specified (workingDir)'
			elif mandatory^15 == 2: print 'ERROR Not all mandatory labels were specified (upCommand)'
			elif mandatory^15 == 4: print 'ERROR Not all mandatory labels were specified (downCommand)'
			elif mandatory^15 == 8: print 'ERROR Not all mandatory labels were specified (configFile)'
			raise NameError(mandatory)
		if block_optional<3 and block_optional != 0:
			if   block_optional^7 == 1: print 'ERROR Not all pos-radius labels were specified (xpos)'
			elif block_optional^7 == 2: print 'ERROR Not all pos-radius labels were specified (ypos)'
			raise NameError(block_optional)
		components.append(comp)
	elif node.type == "text":
		if stringIsUseful(str(node.properties)):
			print '    tssssssss'+str(node.properties)
	else:
		print "error: "+str(node.name)
	
	comp.setGraphicsData()
	comp.CheckItem.initializeComponent(comp)
	comp.CheckItem.start()
	print "Got information of " +comp.alias
def parseSingleValue(node, arg, doCheck=True, optional=False):
	if node.children != None and doCheck == True: print 'WARNING: No children expected'+str(node)
	if not node.hasProp(arg) and not optional:
		print 'WARNING: ' + arg + ' attribute expected'
	else:
		ret = node.prop(arg)
		node.unsetProp(arg)
		return ret

def parseIcon(node, comp):
	x = parseSingleValue(node, 'value', optional=True)
	try:
		icon=QtGui.QPixmap(x)
		comp.graphicsItem.setIcon(icon)
		comp.DirectoryItem.setIcon(icon)
		comp.IconFilePath=x
		if icon.isNull():
			raise NameError("Wrong file Path Given on item")
	except:
		print "Icon file path incorrect>>Icon set to default Value"     
		comp.IconFilePath=os.getcwd()+"/share/rcmanager/1465594390_sign-add.png" #THis is the default icon can be changed by users choice
		icon=QtGui.QPixmap(comp.IconFilePath)
		comp.graphicsItem.setIcon(icon)
		comp.DirectoryItem.setIcon(icon)

def getXmlFromNetwork(dict, components):
	string=''
	string=string+'<?xml version="1.0" encoding="UTF-8"?>\n'
	string=string+'<rcmanager>\n\n'
	string=string+'\t<generalInformation>\n'

	#To be edited as setting increases

	string=string+'\n\t</generalInformation>\n'
	
	for comp in components:
		comp.x=comp.graphicsItem.x()
		comp.y=comp.graphicsItem.y()
		string=string+'\n\t<node alias="' + comp.alias + '" endpoint="' + comp.endpoint + '">\n'
		for dep in comp.dependences:
			string=string+'\t\t<dependence alias="' + dep + '" />\n'
		string=string+'\t\t<workingDir path="' + comp.workingdir + '" />\n'
		string=string+'\t\t<upCommand command="' + comp.compup + '" />\n'
		string=string+'\t\t<downCommand command="' + comp.compdown + '" />\n'
		string=string+'\t\t<configFile path="' + comp.configFile + '" />\n'
		string=string+'\t\t<xpos value="' + str(comp.x) + '" />\n'
		string=string+'\t\t<ypos value="' + str(comp.y) + '" />\n'
		string=string+'\t\t<icon value="'+str(comp.IconFilePath)+'"/>\n'
		string=string+'\t\t<ip value="'+str(comp.Ip)+'"/>\n'
		string=string+'\t</node>\n'

	string=string+'\n</rcmanager>'
	return string

def writeToFile(file, string):#Write a line to the file
	file.write((string).encode( "utf-8" ))

def getDefaultNode():
	string="\n"
	string=string+ '\t<node alias=" " endpoint=" ">\n'
	string=string+ '\t\t<dependence alias=" " />\n'
	string=string+ '\t\t<workingDir path=" " />\n'
	string=string+ '\t\t<upCommand command=" " />\n'
	string=string+ '\t\t<downCommand command=" " />\n'
	string=string+ '\t\t<configFile path=" " />\n'
	string=string+ '\t\t<xpos value=" " />\n'
	string=string+ '\t\t<ypos value=" " />\n'
	string=string+ '\t\t<icon value=" "/>\n'
	string=string+ '\t\t<ip value=" "/>\n'
	string=string+ '\t</node>\n'
	return string