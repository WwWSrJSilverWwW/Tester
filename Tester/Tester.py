import sys
from build.SalutatoryPr import Salutatory
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
begin = Salutatory()
begin.show()
sys.exit(app.exec_())
