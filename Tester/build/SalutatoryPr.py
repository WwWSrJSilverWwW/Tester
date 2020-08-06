import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from build.AuthorizationPr import Authorization
from build.TestControlPr import TestControl
from build.TestTrainingPr import TestTraining
from build.ResultsPr import Results
from build.DataBaseSy import sql_do_something
from build.OptionsSy import *


class Salutatory(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('build\Designers\SalutatoryDes.ui', self)
        self.setFixedSize(int(1 / 3 * fixedSize[0]), int(2 / 3 * fixedSize[1]))
        x = (QApplication.desktop().width() - self.size().width()) // 2
        y = (QApplication.desktop().height() - self.size().height()) // 2
        self.setGeometry(x, y, self.size().width(), self.size().height())
        self.setWindowTitle(RU_LABELS["salutatory"])
        self.kontrTest.clicked.connect(self.kontrTest_def)
        self.trainTest.clicked.connect(self.trainTest_def)
        self.results.clicked.connect(self.results_def)
        self.authorization.clicked.connect(self.authorization_def)
        self.exit.clicked.connect(self.closeEvent)
        self.pupils.addItems([x[0] for x in sql_do_something(dataBase, """SELECT DISTINCT result_name FROM results 
            WHERE result_name <> '' ORDER BY result_name""")])
        self.pupils.activated[str].connect(self.pupils_def)
        self.tests.addItems([x[0] for x in sql_do_something(dataBase, """SELECT DISTINCT test_name FROM tests 
            ORDER BY test_name""")])
        self.tests.activated[str].connect(self.tests_def)
        self.setFocusPolicy(Qt.StrongFocus)

    def kontrTest_def(self):
        if len(sql_do_something(dataBase, f"""SELECT test_id FROM tests WHERE test_name 
             = '{self.testName.text()}'""")) == 0:
            QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["chooseGoodTest"])
        else:
            self.kt = TestControl(self.testName.text(), self.pupilName.text())
            self.pupilName.setText("Без имени")
            self.testName.clear()
            self.kt.show()

    def trainTest_def(self):
        if len(sql_do_something(dataBase, f"""SELECT test_id FROM tests WHERE test_name 
             = '{self.testName.text()}'""")) == 0:
            QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["chooseGoodTest"])
        else:
            self.tt = TestTraining(self.testName.text(), self.pupilName.text())
            self.pupilName.setText("Без имени")
            self.testName.clear()
            self.tt.show()

    def results_def(self):
        self.res = Results()
        self.res.show()

    def authorization_def(self):
        self.auth = Authorization()
        self.auth.show()

    def closeEvent(self, event):
        sys.exit()

    def pupils_def(self, text):
        self.pupilName.setText(text)

    def tests_def(self, text):
        self.testName.setText(text)

    def focusInEvent(self, event):
        self.pupils.clear()
        self.tests.clear()
        self.pupils.addItems([x[0] for x in sql_do_something(dataBase, """SELECT DISTINCT result_name FROM results 
            WHERE result_name <> '' ORDER BY result_name""")])
        self.tests.addItems([x[0] for x in sql_do_something(dataBase, """SELECT DISTINCT test_name FROM tests 
            ORDER BY test_name""")])
