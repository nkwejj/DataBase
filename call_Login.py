# 导入程序运行必须模块
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
# 导入designer工具生成的login模块
import pymysql
from Login import Ui_MainWindow
from student import Ui_Student
from teacher import Ui_Teacher



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)


class Student_Form(QMainWindow, Ui_Student):
    def __init__(self, parent=None):
        super(Student_Form, self).__init__(parent)
        self.setupUi(self)


class Teacher_Form(QMainWindow, Ui_Teacher):
    def __init__(self, parent=None):
        super(Teacher_Form, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    stuWin = Student_Form()
    teaWin = Teacher_Form()

    def login():
        user = myWin.lineEdit.text()
        pwd = myWin.lineEdit_2.text()

        db = pymysql.connect(host='localhost', user='root', password='123456', database='eams', charset='utf8mb4')
        cursor = db.cursor()
        sql = "SELECT student_id FROM student where student_id = '%s' and student_id = '%s'" % (user, pwd)
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            cursor = db.cursor()
            sql = "SELECT teacher_id FROM teacher where teacher_id = '%s' and teacher_id = '%s'" % (user, pwd)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                # teacher和student都没有
                myWin.textBrowser.setText("用户名或密码错误，请重新输入!")
                myWin.textBrowser.repaint()
            else:
                # teacher
                myWin.textBrowser.setText("欢迎%s" % user)
                myWin.textBrowser.repaint()
                teaWin.tea_ui(str(result[0][0]))

                myWin.close()
                teaWin.show()
        else:
            # student
            myWin.textBrowser.setText("欢迎%s" % user)
            myWin.textBrowser.repaint()
            stuWin.stu_ui(str(result[0][0]))

            myWin.close()
            stuWin.show()

        cursor.close()
        db.close()


    myWin.pushButton.clicked.connect(login)
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
