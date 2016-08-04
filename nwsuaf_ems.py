# coding=utf-8
# nwsuaf_ems.py
"""
Graphical interface of NWSUAF_EMS.py
"""
import sys
import re
from PyQt4 import QtGui, QtCore
from Crawler import NWSUAF_EMS

# using object-oriented method
class Gi_NWSUAF_EMS(QtGui.QWidget):
    """
    Encapsulation QtGui.QWidget class.
    """
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        # table with columns and rows
        self.table = QtGui.QTableWidget(self)
        # year
        self.year_box = QtGui.QComboBox(self)
        # term
        self.term_box = QtGui.QComboBox(self)
        # query
        self.query = QtGui.QPushButton('Query', self)
        # student id
        self.student_id = QtGui.QLineEdit(self)
        # name
        self.name = QtGui.QLineEdit(self)
        self.init()
        self.init_layout()
        self.init_connect()
        # store data
        self.year_box_select = None
        self.term_box_select = None
        self.id = None
        self.password = None
        # init emit signals
        self.init_emit()

    def set_col(self, columns):
        """
        Set table columns.
        :param columns: int
        :return:
        """
        self.table.setColumnCount(columns)

    def set_row(self, rows):
        """
        Set table rows.
        :param rows: int
        :return:
        """
        self.table.setRowCount(rows)

    def init_emit(self):
        """
        :return:
        """
        self.year_box.emit(QtCore.SIGNAL('activated(int)'), 0)
        self.term_box.emit(QtCore.SIGNAL('activated(int)'), 0)

    def init(self):
        """
        Init year_box and term_box.
        :return:
        """
        # set year_box
        str_list = QtCore.QStringList()
        str_list << '2016' << '2015' << '2014'
        self.year_box.addItems(str_list)
        # set term_box
        str_list.clear()
        str_list << 'All' << 'Spring' << 'Autumn'
        self.term_box.addItems(str_list)
        # set table headers
        str_list.clear()
        str_list << u'学年' << u'学期' <<u'课程号' << u'课程名'<<u'课序号' << u'平时' << u'期中' << u'期末' \
                 << u'实验' << u'总评' << u'学分' << u'学时' << u'考核方式' << u'选课属性' \
                 << u'备注' << u'考试性质' << u'是否缓考' << u'二学位/辅考' << u'及格标志'
        self.table.setColumnCount(19)
        self.table.setHorizontalHeaderLabels(str_list)

    def init_connect(self):
        """
        Connect signals and slots.
        :return:
        """
        self.connect(self.year_box, QtCore.SIGNAL('activated(int)'), self, QtCore.SLOT('year_slot(int)'))
        self.connect(self.term_box, QtCore.SIGNAL('activated(int)'), self, QtCore.SLOT('term_slot(int)'))
        self.connect(self.query, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('query_slot()'))

    def init_layout(self):
        """
        Set layout.
        :return:
        """
        # QHBoxLayout
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        label_student_id = QtGui.QLabel('StudentId:', self)
        hbox.addWidget(label_student_id)
        hbox.addWidget(self.student_id)
        label_name = QtGui.QLabel('Password:', self)
        hbox.addWidget(label_name)
        hbox.addWidget(self.name)
        label__year = QtGui.QLabel('Year:', self)
        hbox.addWidget(label__year)
        hbox.addWidget(self.year_box)
        label__term = QtGui.QLabel('Term:', self)
        hbox.addWidget(label__term)
        hbox.addWidget(self.term_box)
        hbox.addWidget(self.query)
        hbox.addStretch(1)
        # QVBoxLayout
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)
        # SetLayout
        self.setLayout(vbox)

    @property
    def start_grap(self):
        """
        :return: list[list[]]
        """
        # NWSUAF_EMS object
        splider = NWSUAF_EMS.NWSUAF_EMS()
        # set id and password
        splider.set_data(self.id, self.password)
        # get captcha
        splider.get_captcha()
        # input captcha
        captcha, result = QtGui.QInputDialog.getText(self, 'Captcah', 'Input Captcha:')
        if not result:
            return None
        else:
            # login
            splider.get_index_page(str(captcha))
            # score page
            splider.get_score_page()
            return splider.get_score_page_item()

    @QtCore.pyqtSlot(int)
    def year_slot(self, arg1):
        """
        :param arg1: int
        :return:
        """
        self.year_box_select = arg1

    @QtCore.pyqtSlot(int)
    def term_slot(self, arg1):
        """
        :param arg1: int
        :return:
        """
        self.term_box_select = arg1

    @QtCore.pyqtSlot()
    def query_slot(self):
        """
        :return:
        """
        # get student id and password
        self.id = str(self.student_id.text())
        self.password = str(self.name.text())
        # re checks if it is legal
        pattern = r'(\d){10}'
        pattern = re.compile(pattern)
        if re.match(pattern, self.id) and len(self.id)==10:
            if self.password == '':
                QtGui.QMessageBox.information(self, 'Message', 'student password is empty!')
            else:
                # start grap data
                items = self.start_grap
                if items is None:
                    QtGui.QMessageBox.information(self, 'Message', 'check your password or captcha!')
                    return None
                self.table.setRowCount(len(items))
                for i in xrange(len(items)):
                    sign = 0
                    for j in xrange(len(items[i])):
                        if j == 9:
                            sign = 1
                        if j == len(items[i])-1:
                            break
                        self.table.setItem(i, j, QtGui.QTableWidgetItem(items[i][j+sign].decode('utf-8')))
        else:
            QtGui.QMessageBox.information(self, 'Message', 'student id illegal!')


if __name__ == '__main__':
    # application object
    app = QtGui.QApplication(sys.argv)

    win = Gi_NWSUAF_EMS()
    win.show()

    # exit after message loop
    sys.exit(app.exec_())