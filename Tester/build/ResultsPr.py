from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from build.DataBaseSy import sql_do_something
from build.OptionsSy import *


class Results(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('build\Designers\ResultsDes.ui', self)
        self.setFixedSize(*fixedSize)
        x = (QApplication.desktop().width() - self.size().width()) // 2
        y = (QApplication.desktop().height() - self.size().height()) // 2
        self.setGeometry(x, y, self.size().width(), self.size().height())
        self.setWindowTitle(RU_LABELS["results"])
        self.model = QStandardItemModel()
        self.resultsTable.setModel(self.model)
        self.results = sql_do_something(dataBase, "SELECT * FROM results")
        self.load_data(len(self.results), len(self.results[0]), self.results)
        self.model.setHorizontalHeaderLabels(RU_LABELS["tableHeadings"])

    def load_data(self, n, m, data):
        self.model.setRowCount(n)
        self.model.setColumnCount(m - 1)
        for i in range(n):
            for j in range(m - 1):
                if j == 0:
                    item = QStandardItem(sql_do_something(dataBase, f"""SELECT test_name FROM tests WHERE test_id = 
                        {data[i][j + 1]}""")[0][0])
                elif j == 1 and data[i][j + 1] == "":
                    item = QStandardItem(RU_LABELS["noName"])
                else:
                    item = QStandardItem(str(data[i][j + 1]))
                self.model.setItem(i, j, item)
