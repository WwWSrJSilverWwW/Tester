from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from build.DataBaseSy import sql_do_something
from build.OptionsSy import *


class TestControl(QMainWindow):
    def __init__(self, test_name, pupil_name):
        super().__init__()
        uic.loadUi('build\Designers\TestControlDes.ui', self)
        self.setFixedSize(self.size())
        self.setWindowTitle(RU_LABELS["testControl"])
        self.pupil_name = pupil_name
        self.test_name = test_name
        self.test = sql_do_something(dataBase, f"""SELECT * FROM quests WHERE test_id IN (SELECT test_id FROM tests 
            WHERE test_name = '{self.test_name}')""")
        self.test.sort(key=lambda x: x[6])
        self.now = 0
        self.ans = 0
        self.max = 0
        self.k = 0
        self.time_of_pupil = 0
        self.quest = ['0'] * 8
        self.btn_group = []
        self.contin.clicked.connect(self.contin_def)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.contin_def)
        self.quest_time = sql_do_something(dataBase, f"""SELECT test_long FROM tests WHERE test_name = 
            '{self.test_name}'""")[0][0] // len(self.test)
        self.timer.start(self.quest_time * 1000)
        self.questDuration.setText(str(self.quest_time))
        self.timer_for_time = QTimer(self)
        self.timer_for_time.timeout.connect(self.go_on_time)
        self.timer_for_time.start(1000)
        self.contin_def()

    def contin_def(self):
        if self.now < len(self.test):
            right_answers = list(map(int, self.quest[7].split("|%$#")))
            for i in range(len(self.btn_group)):
                if self.btn_group[i].isChecked():
                    if i + 1 in right_answers:
                        self.ans += 1
                    else:
                        self.ans -= 1
                if i + 1 in right_answers:
                    self.max += 1

            self.maxGood.setText(str(self.max))
            self.nowGood.setText(str(self.ans))
            self.time_of_pupil += self.timer.remainingTime() // 1000

            self.btn_group = []
            for i in reversed(range(self.verticalLayout.count())):
                self.verticalLayout.itemAt(i).widget().deleteLater()

            self.quest = self.test[self.now]
            self.questLabel.setText(self.quest[2])
            x = 0
            for answer in self.quest[3].split("|%$#"):
                if self.quest[1] == '1':
                    x = QRadioButton(answer)
                elif self.quest[1] == '2':
                    x = QCheckBox(answer)
                self.verticalLayout.addWidget(x)
                self.btn_group.append(x)
            self.now += 1
            self.k = 0
            self.nowTime.setText("0")
            self.timer.stop()
            self.timer.start()
            self.timer_for_time.stop()
            self.timer_for_time.start()
        else:
            self.timer.stop()
            self.timer_for_time.stop()
            right_answers = list(map(int, self.quest[7].split("|%$#")))
            for i in range(len(self.btn_group)):
                if self.btn_group[i].isChecked():
                    if i + 1 in right_answers:
                        self.ans += 1
                    else:
                        self.ans -= 1
                if i + 1 in right_answers:
                    self.max += 1

            self.maxGood.setText(str(self.max))
            self.nowGood.setText(str(self.ans))
            self.time_of_pupil += self.quest_time - self.timer.remainingTime() // 1000 - 1

            k = sql_do_something(dataBase, f"""SELECT test_id FROM tests WHERE test_name = 
                '{self.test_name}'""")[0][0]
            sql_do_something(dataBase, f"""INSERT INTO results (test_id, result_name, result_answer, 
                result_duration) VALUES({k}, '{self.pupil_name}', '{str(self.ans) + ";" + str(self.max)}', 
                {self.time_of_pupil})""")
            marks = list(reversed(list(map(float, sql_do_something(dataBase, f"""SELECT test_marks FROM tests WHERE 
                test_name = '{self.test_name}'""")[0][0].split(";")))))
            proc = self.ans / self.max * 100
            marks.append(proc)
            marks.sort()
            mark = marks.index(proc)
            if mark != 5 and marks[mark + 1] == proc:
                mark += 1
            if mark == 0:
                mark = 1
            QMessageBox.about(self, RU_LABELS["result"],
                              f"{self.pupil_name}, Ваш результат - {self.ans} из {self.max}.\nВаша оценка - {mark}.")

            self.close()

    def go_on_time(self):
        self.k += 1
        self.nowTime.setText(str(self.k))
