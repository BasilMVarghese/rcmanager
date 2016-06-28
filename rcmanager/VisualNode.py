##
#This module is for defining the nodes on the component tree.This will basically contain the QGraphicsItems to be di
#Displayed on the graphicsScene of the component network
##



from PyQt4 import QtCore, QtGui

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

class VisualNode(QtGui.QGraphicsItem):
	"""docstring for ClassName"""
	def __init__(self, view=None,Alias=None,arg=None):
		QtGui.QGraphicsItem.__init__(self,arg)
		self.view=view
		self.Alias=Alias
		self.pos=None
		self.Iconfile=None
		self.IpColor=None
	def setview(view):
		self.view=view
	def boundingRect(self):
		self.penWidth =2
		return QtCore.QRectF(-49,-49,98,98)
	def paint(self,painter,option=None,widget=None):
		self.paintMainShape(painter)
		self.drawStatus(painter)
		self.drawIcon(painter)
		self.writeAlias(painter)
	def setIcon(self,filepath):
		print "Icon setting"
		self.Icon=QtGui.QPixmap(filepath)
	def paintMainShape(self,painter): ##This will draw the basic shape of a node.The big square and its containing elements
		pen=QtGui.QPen(QtGui.QColor.fromRgb(0,0,0))
		pen.setWidth(3)
		painter.setPen(pen)
		brush=QtGui.QBrush(QtGui.QColor.fromRgb(94,94,94))
		painter.setBrush(brush)
		painter.drawRoundedRect(-49,-49,98,98,5,5)
		brush.setColor(QtGui.QColor.fromRgb(255,255,255))
		painter.setBrush(brush)

		self.TextRect=QtCore.QRect(-45,-45,90,20)##The rectangle shape on which the alias name will be dispalyed
		self.statusRect=QtCore.QRect(22,10,20,20)##The rectange shape on which the status of the node will be displayed
		self.IconRect=QtCore.QRect(-45,-20,60,64)## The rectange shape on which the Icon will be displayed
		self.drawConnection(painter,"UP","INCOMMING")
		self.drawConnection(painter,"RIGHT","OUTGOING")
		painter.drawRect(self.TextRect) ##Drawing the Alias display rectangle

		painter.setBrush(self.IpColor)  ## Drawing the Icon display rectangle
		painter.drawRect(self.IconRect)
		
		
	def drawConnection(self,painter,edge="UP",DIRECTION="INCOMMING",dist=0):##This is used to draw the exit and entry points of connections on the node
		if edge=="UP":
			if DIRECTION=="INCOMMING":
				Arrow=QtGui.QPixmap("share/rcmanager/downconnection.png")
				painter.drawPixmap(-49+21*(dist),-69,20,20,Arrow,0,0,0,0)
			elif DIRECTION=="OUTGOING":
				Arrow=QtGui.QPixmap("share/rcmanager/upconnection.png")
				painter.drawPixmap(-49+21*(dist),-69,20,20,Arrow,0,0,0,0)
		elif edge=="DOWN":
			if DIRECTION=="INCOMMING":
				Arrow=QtGui.QPixmap("share/rcmanager/upconnection.png")
				painter.drawPixmap(-49+21*(dist),49,20,20,Arrow,0,0,0,0)
			elif DIRECTION=="OUTGOING":
				Arrow=QtGui.QPixmap("share/rcmanager/downconnection.png	")
				painter.drawPixmap(-49+21*(dist),49,20,20,Arrow,0,0,0,0)
			
		elif edge=="LEFT":
			if DIRECTION=="INCOMMING":
				Arrow=QtGui.QPixmap("share/rcmanager/rightconnection.png")
				painter.drawPixmap(-69,-49+21*(dist),20,20,Arrow,0,0,0,0)
			elif DIRECTION=="OUTGOING":
				Arrow=QtGui.QPixmap("share/rcmanager/leftconnection.png")
				painter.drawPixmap(-69,-49+21*(dist),20,20,Arrow,0,0,0,0)
			
		elif edge=="RIGHT":
			if DIRECTION=="INCOMMING":
				Arrow=QtGui.QPixmap("share/rcmanager/leftconnection.png")
				painter.drawPixmap(49,-49+21*(dist),20,20,Arrow,0,0,0,0)
			elif DIRECTION=="OUTGOING":
				Arrow=QtGui.QPixmap("share/rcmanager/rightconnection.png")
				painter.drawPixmap(49,-49+21*(dist),20,20,Arrow,0,0,0,0)
	def drawIcon(self,painter):#Draw the Icon representing the purpose and draw its 
			painter.setBrush(self.IpColor)  ## Drawing the Icon display rectangle
			painter.drawRect(self.IconRect)
			painter.drawPixmap(-45,-20,60,60,self.Icon,0,0,0,0)
	def writeAlias(self,painter):##Draw the alias
			painter.drawText(self.TextRect,1," "+"SIMULATION") 	##Drawing the Alias name
	def drawStatus(self,painter,color=QtGui.QColor.fromRgb(255,0,0)):
		brush=QtGui.QBrush(color) ##Drawing the Status display rectangle
		painter.setBrush(brush)
		painter.drawRect(self.statusRect)
	

