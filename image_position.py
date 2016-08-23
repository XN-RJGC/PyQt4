# coding: utf-8
from PyQt4.QtWebKit import *
from PyQt4 import QtGui, QtCore
import sys
import piexif

class MainWindow(QtGui.QWidget):
    """
    Encapsulation QtGui.QMainWindow class.
    """
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        # longitude
        self.longitude = None
        # latitude
        self.latitude = None
        # LineEdit
        self.line_edit = QtGui.QLineEdit(self)
        # select QPushButton
        self.select = QtGui.QPushButton('Select', self)
        # position QPushButton
        self.position = QtGui.QPushButton('Position', self)

        self.construct_layout()
        self.init_connect()

    def init_connect(self):
        """
        Connect signals with slots.
        :return:
        """
        self.connect(self.position, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('reload()'))
        self.connect(self.select, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('get_data()'))

    def construct_layout(self):
        """
        Set layout.
        :return:
        """
        # HBoxLayout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.line_edit)
        hbox.addWidget(self.select)
        hbox.addWidget(self.position)
        # VBoxLayout
        vbox = QtGui.QVBoxLayout()
        # construct QWebView
        self.webview = QWebView(self)
        self.webview.load(QtCore.QUrl('http://map.baidu.com/'))
        vbox.addLayout(hbox)
        vbox.addWidget(self.webview)

        # set layout
        self.setLayout(vbox)

    def d2l(self, gpsData):
        """
        # GPS经纬度元组转经纬度
        :param gpsData:
        :return:
        """
        d = gpsData[0][0] / float(gpsData[0][1])  # 度
        m = gpsData[1][0] / float(gpsData[1][1])  # 分
        s = gpsData[2][0] / float(gpsData[2][1])  # 秒
        return str(d + (m + s / 60.0) / 60.0)

    @QtCore.pyqtSlot()
    def reload(self):
        print 'test'
        #self.webview.load(QtCore.QUrl('http://map.baicu.com'))
        #self.webview.load(QtCore.QUrl('http://api.map.baicu.com/geocoder?location= %s,%s&coord_type=gcj02&'
        #                               'output=html&src=personal|ima_pos' % (self.latitude, self.longitude)))
        url = 'http://api.map.baidu.com/geocoder?location=39.990912172420714,116.32715863448607&coord_type=gcj02&output=html&src=yourCompanyName|yourAppName'
        self.webview.load(QtCore.QUrl(url))

    @QtCore.pyqtSlot()
    def get_data(self):
        """
        Get picture exif'GPS information
        :return:
        """
        file_dialog = QtGui.QFileDialog()
        file_name = file_dialog.getOpenFileName()
        # self.line_edit set text
        self.line_edit.setText(str(file_name))
        # load picture and get exif data as dict
        exif_data = piexif.load(str(file_name))

        if exif_data['GPS']:
            print exif_data['GPS']
            for key, value in exif_data['GPS'].items():
                print key, value
            try:
                self.latitude = self.d2l(exif_data['GPS'].get(7))
                self.longitude = self.d2l(exif_data['GPS'].get(7))
                print 'latitude: %s' % self.latitude
                print 'longitude: %s' % self.longitude
            except:
                QtGui.QMessageBox.information(self, 'Message', 'Get latitude and longitude error!')
        else:
            QtGui.QMessageBox.information(self, 'Message', 'This picture has not GPS information!')

if __name__ == '__main__':
    # application object
    app = QtGui.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    # exit after message loop
    sys.exit(app.exec_())