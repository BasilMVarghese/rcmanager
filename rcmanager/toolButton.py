from PyQt4 import QtCore,QtGui

class toolButton(QtGui.QToolButton):
	def  __init__(self,parent):
		QtGui.QToolButton.__init__(self,parent)
		self.setMouseTracking(True)
	def enterEvent(self,event):
		self.emit(QtCore.SIGNAL("hovered()"))
		QtGui.QToolButton.enterEvent(self,event)