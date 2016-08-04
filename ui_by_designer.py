# ui_by_designer.py
"""
ui by qt4-designer
"""
import sys
from PyQt4 import QtGui
import untitled

# using object-oriented method
class uibydesigner(QtGui.QWidget):
    """
    Encapsulation QtGui.QWidget class.
    """
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = None
        # from ui
        self.login_gui()

    def login_gui(self):
        # type: () -> object
        """
        :rtype: object
        """
        self.ui = untitled.Ui_Form()
        self.ui.setupUi(self)

if __name__ == '__main__':
    # application instance
    app = QtGui.QApplication(sys.argv)

    win = uibydesigner()
    win.show()

    #exit after message loop
    sys.exit(app.exec_())