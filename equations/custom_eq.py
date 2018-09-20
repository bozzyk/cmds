#-*- encoding: utf-8 -*-
from sympy import *
from matplotlib import pyplot as plt
from sys import argv
from timeit import default_timer as timer
#from numba import vectorize, float64,int32
#from numba import jit

import numpy

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#@vectorize([float64[:](float64(float64, float64, float64),float64(float64, float64, float64),float64,float64,float64,int32,float64)], target='cuda')
def my_evaluate(f,g,x0,y0,t0,n,delta_t):

    x,y,t = symbols('x y t')

    dots_x = [x0]
    dots_y = [y0]
    current_t = t0

    k1,k2,k3,k4,m1,m2,m3,m4 = None, None, None, None, None, None, None, None

    for i in range(1,n+1):
        k1 = f(dots_x[i-1],dots_y[i-1],current_t)*delta_t
        m1 = g(dots_x[i-1],dots_y[i-1],current_t)*delta_t

        k2 = f(dots_x[i-1]+k1/2,dots_y[i-1]+m1/2,current_t+delta_t/2)*delta_t
        m2 = g(dots_x[i-1]+k1/2,dots_y[i-1]+m1/2,current_t+delta_t/2)*delta_t

        k3 = f(dots_x[i-1]+k2/2,dots_y[i-1]+m2/2,current_t+delta_t/2)*delta_t
        m3 = g(dots_x[i-1]+k2/2,dots_y[i-1]+m2/2,current_t+delta_t/2)*delta_t

        k4 = f(dots_x[i-1]+k3/2, dots_y[i-1]+m3/2,current_t+delta_t/2)*delta_t
        m4 = g(dots_x[i-1]+k3/2, dots_y[i-1]+m3/2,current_t+delta_t/2)*delta_t

        dots_x.append(dots_x[i-1]+(1/6)*(k1+2*k2+2*k3+k4))
        dots_y.append(dots_y[i-1]+(1/6)*(m1+2*m2+2*m3+m4))
        current_t += delta_t

    return (dots_x, dots_y)


class customEq(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.quitApp)

        saveAction = QAction('Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.showSaveDialog)

        toolbar = QToolBar("smth")
        toolbar.addAction(exitAction)
        toolbar.addAction(saveAction)

        dxt_field = QLineEdit(self)
        dxt_field.setObjectName("dxt_field")
        dxt_lbl = QLabel("dx/dt = ")

        dyt_field = QLineEdit(self)
        dyt_field.setObjectName("dyt_field")
        dyt_lbl = QLabel("dy/dt = ")


        x0_field = QLineEdit(self)
        x0_field.setObjectName("x0_field")
        x0_lbl = QLabel("x0")

        y0_field = QLineEdit(self)
        y0_field.setObjectName("y0_field")
        y0_lbl = QLabel("y0")

        t0_field = QLineEdit(self)
        t0_field.setObjectName("t0_field")
        t0_lbl = QLabel("t0")


        dots_num_field = QLineEdit(self)
        dots_num_field.setObjectName("dots_num_field")
        dots_num_lbl = QLabel("Количество точек")

        time_field = QLineEdit(self)
        time_field.setObjectName("time_field")
        time_lbl = QLabel("'Шаг' времени")

        draw_btn = QPushButton("ОК", self)
        draw_btn.clicked.connect(self.buttonClicked)

        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(dxt_lbl, 0,0)
        grid.addWidget(dyt_lbl, 1,0)
        grid.addWidget(x0_lbl, 2,0)
        grid.addWidget(y0_lbl, 3,0)
        grid.addWidget(t0_lbl, 4,0)
        grid.addWidget(dots_num_lbl, 5,0)
        grid.addWidget(time_lbl, 6,0)


        grid.addWidget(dxt_field, 0,1)
        grid.addWidget(dyt_field, 1,1)
        grid.addWidget(x0_field, 2,1)
        grid.addWidget(y0_field, 3,1)
        grid.addWidget(t0_field, 4,1)
        grid.addWidget(dots_num_field, 5,1)
        grid.addWidget(time_field, 6,1)

        grid.addWidget(draw_btn, 7,1)

        grid.addWidget(toolbar, 8,0)


        self.setLayout(grid)
        self.setGeometry(600, 300, 600, 400)


        self.setWindowTitle('Runge-Kutta custom equation')
        self.show()

    def showSaveDialog(self):

        name = QFileDialog.getSaveFileName(self)
        if name[0]:
            plt.savefig(name[0])

    def quitApp(self):
        self.close()




    def isiterable(self, smth):
        try:
            iterator = iter(smth)
        except TypeError:
            return False
        else:
            return True

    def inner_evaluate(self, *args):
        return my_evaluate(*args)

    def buttonClicked(self):

        x,y,t = symbols('x y t')

        f = lambdify([x,y,t],eval(self.findChild(QLineEdit, "dxt_field").text()), numpy)
        g = lambdify([x,y,t],eval(self.findChild(QLineEdit, "dyt_field").text()), numpy)

        n = int(self.findChild(QLineEdit, "dots_num_field").text())
        delta_t = eval(self.findChild(QLineEdit, "time_field").text())

        t0 = eval(self.findChild(QLineEdit, "t0_field").text())
        x0 = eval(self.findChild(QLineEdit, "x0_field").text())
        y0 = eval(self.findChild(QLineEdit, "y0_field").text())

        start = timer()
        if not self.isiterable(x0) and not self.isiterable(y0) and not self.isiterable(t0):
            data = self.inner_evaluate(f,g,x0,y0,t0,n,delta_t)
        else:
            data = [(self.inner_evaluate(f,g,i,j,k,n,delta_t)[0], self.inner_evaluate(f,g,i,j,k,n,delta_t)[1]) for i,j,k in zip(x0,y0,t0)]
        fst_time = timer()-start
        print(fst_time)

        start = timer()
        if not self.isiterable(data[0][0]):
            plt.scatter(data[0],data[1],c='r',s=1)
        else:
            for (i,j) in data:
                plt.scatter(i,j,c='r', s=1)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(u"метод Рунге-Кутты")
        plt.savefig('plot.png')
        plt.grid()
        snd_time = timer()-start
        print (snd_time)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = customEq()
    sys.exit(app.exec_())
