# PyGlassBasicDialogManager.py
# (C)2012
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

#___________________________________________________________________________________________________ PyGlassBasicDialogManager
class PyGlassBasicDialogManager(QtCore.QObject):

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ openAbout
    @classmethod
    def openAbout(cls, parent, title, text):
        return QtGui.QMessageBox.about(parent=parent, title=title, text=text)

#___________________________________________________________________________________________________ openYesNo
    @classmethod
    def openYesNo(cls, parent, header, message =None, defaultToYes =True):
        dlg = QtGui.QMessageBox(parent=parent)
        dlg.setText(header)
        if message:
            dlg.setInformativeText(message)
        dlg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        dlg.setDefaultButton(QtGui.QMessageBox.Yes if defaultToYes else QtGui.QMessageBox.No)
        result = dlg.exec_()
        return result == QtGui.QMessageBox.Yes

#___________________________________________________________________________________________________ openOk
    @classmethod
    def openOk(cls, parent, header, message =None):
        dlg = QtGui.QMessageBox(parent=parent)
        dlg.setText(header)
        if message:
            dlg.setInformativeText(message)
        dlg.setStandardButtons(QtGui.QMessageBox.Ok)
        dlg.setDefaultButton(QtGui.QMessageBox.Ok)
        result = dlg.exec_()
        return True

#___________________________________________________________________________________________________ openTextQuery
    @classmethod
    def openTextQuery(cls, parent, header, message =None, defaultText =None):
        if defaultText is None:
            defaultText = u''
        return QtGui.QInputDialog.getText(parent, header, message, text=defaultText)
