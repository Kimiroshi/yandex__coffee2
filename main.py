import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import uic

import sqlite3

con = sqlite3.connect('coffee.sqlite')
cur = con.cursor()


class AddEditCoffeeForm(QWidget):
    def __init__(self, arg):
        self.arg = arg
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.pushButton.clicked.connect(self.add)

    def add(self):
        print(True)
        id = str(self.lineEdit1.text())
        name = str(self.lineEdit2.text())
        roast = str(self.lineEdit3.text())
        cond = str(self.lineEdit4.text())
        taste = str(self.lineEdit5.text())
        price = int(self.lineEdit6.text())
        size = int(self.lineEdit7.text())
        try:
            if len(cur.execute(f'SELECT * From coffee WHERE id = {int(id)}').fetchall()) == 0:
                cur.execute(f'''INSERT INTO coffee('ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 
                'Описание вкуса', 'Цена', 'Объем упаковки') VALUES(?, ?, ?, ?, ?, ?, ?)''',
                            (id, name, roast, cond, taste, price, size))
                con.commit()
            else:
                cur.execute(
                    f'''UPDATE coffee SET 'Название сорта' = '{name}', 'Степень обжарки' = '{roast}', 
                    'Молотый/в зернах' = '{cond}', 'Описание вкуса' = '{taste}',
                'Цена' = {price}, 'Объем упаковки' = {size} WHERE id = {id}''')
                con.commit()
            self.arg.loadTable()
        except Exception as ex:
            print(ex)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.loadTable()
        self.addButton.clicked.connect(self.show_)

    def loadTable(self):
        reader = [['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                   'Объем упаковки']]
        res = cur.execute(f'''SELECT * From coffee''').fetchall()
        for i in range(len(res)):
            res[i] = list(res[i])
        reader += res
        title = reader[0]
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(reader[1::]):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def show_(self):
        global ex1
        ex1 = AddEditCoffeeForm(self)
        ex1.show()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
