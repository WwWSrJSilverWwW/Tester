from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from build.DataBaseSy import sql_do_something
from build.OptionsSy import *


class MakingTest(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('build\Designers\MakingTestDes.ui', self)
        self.setFixedSize(self.size())
        self.setWindowTitle(RU_LABELS["makingTest"])
        self.add.clicked.connect(self.add_def)
        self.types.clear()
        self.types.addItems([x[0].upper() + x[1:] for x in primitiveQuestions])
        self.types.activated[str].connect(self.type_def)
        self.saveTest.clicked.connect(self.close)
        self.test_id = max(x[0] for x in (sql_do_something(dataBase, "SELECT test_id FROM tests") + [(0,)])) + 1
        self.testNumber.setText(f"<b>Тест #{self.test_id}</b>")
        self.test_zs = []
        self.order = 1
        self.five.setValue(90)
        self.four.setValue(70)
        self.three.setValue(50)
        self.two.setValue(30)
        self.one.setValue(10)
        time = QTime()
        time.setHMS(0, 45, 0)
        self.testDuration.setDisplayFormat('hh:mm:ss')
        self.testDuration.setTime(time)

    def closeEvent(self, event):
        button_reply = QMessageBox.question(self, RU_LABELS["warning"], RU_LABELS["saveTest?"],
                                            QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        if button_reply == QMessageBox.Save:
            marks_data = list(map(str, [self.five.value(), self.four.value(), self.three.value(), self.two.value(),
                                        self.one.value()]))
            if not all(int(marks_data[i]) > int(marks_data[i + 1]) for i in range(4)):
                QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["percentage"])
                event.ignore()
            else:
                marks = ";".join(marks_data)
                for z in self.test_zs:
                    sql_do_something(dataBase, z)
                sql_do_something(dataBase, f"""INSERT INTO tests (test_name, test_marks, test_author, test_long) 
                    VALUES('{self.testName.text()}', '{marks}', '{self.testAuthor.text()}', {
                    self.testDuration.time().hour() * 3600 + self.testDuration.time().minute() * 60 + 
                    self.testDuration.time().second()})""")
                event.accept()
        elif button_reply == QMessageBox.No:
            event.accept()
        elif button_reply == QMessageBox.Cancel:
            event.ignore()

    def add_def(self):
        if self.type.text() == "" or self.question.toPlainText() == "" or self.answers.toPlainText() == "" \
                or self.rightIndexes.text() == "":
            QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["somethingClear"])
        else:
            if self.type.text().lower() not in primitiveQuestions:
                QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["notExist"])
            else:
                tip = self.type.text().lower()
                quest = self.question.toPlainText()
                ans = self.answers.toPlainText().strip("\n")
                right_ind = self.rightIndexes.text()
                answers = "|%$#".join(ans.split("\n"))
                right = "|%$#".join(right_ind.split())
                if tip == primitiveQuestions[0]:
                    if len(self.rightIndexes.text().split()) > 1:
                        QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["oneOnly"])
                    else:
                        self.test_zs.append(f"""INSERT INTO quests (quest_type, quest_name, quest_answers, test_id, 
                            quest_long, quest_order, quest_right_answers_indexes) VALUES(1, '{quest}', '{answers}', 
                            {self.test_id}, 30, {self.order}, '{right}')""")
                        self.order += 1
                        self.question.clear()
                        self.answers.clear()
                        self.rightIndexes.clear()
                        k = ans.replace("\n", "; ")
                        self.questsView.addItem(f"""Вопрос типа "Обычный": {quest}\nОтветы: {k}\nПравильный ответ: {right_ind}\n""")
                elif tip == primitiveQuestions[1]:
                    if len(self.rightIndexes.text().split()) > len(self.answers.toPlainText().rstrip("\n").split("\n")):
                        QMessageBox.about(self, RU_LABELS["warning"], RU_LABELS["moreGoodAnswers"])
                    else:
                        self.test_zs.append(f"""INSERT INTO quests (quest_type, quest_name, quest_answers, test_id, 
                            quest_long, quest_order, quest_right_answers_indexes) VALUES(2, '{quest}', '{answers}', 
                            {self.test_id}, 30, {self.order}, '{right}')""")
                        self.order += 1
                        self.question.clear()
                        self.answers.clear()
                        self.rightIndexes.clear()
                        k = ans.replace("\n", "; ")
                        self.questsView.addItem(f"""Вопрос типа "Множественный": {quest}\nОтветы: {k}\nПравильные ответы: {right_ind}\n""")

    def type_def(self, text):
        self.type.setText(text)
