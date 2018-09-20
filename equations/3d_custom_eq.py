from sympy import *
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *






class custom3DEq(QWidget):
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

        dzt_field = QLineEdit(self)
        dzt_field.setObjectName("dzt_field")
        dzt_lbl = QLabel("dz/dt = ")


        x0_field = QLineEdit(self)
        x0_field.setObjectName("x0_field")
        x0_lbl = QLabel("x0")

        y0_field = QLineEdit(self)
        y0_field.setObjectName("y0_field")
        y0_lbl = QLabel("y0")

        z0_field = QLineEdit(self)
        z0_field.setObjectName("z0_field")
        z0_lbl = QLabel("z0")

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
        grid.addWidget(dzt_lbl, 2,0)
        grid.addWidget(x0_lbl, 3,0)
        grid.addWidget(y0_lbl, 4,0)
        grid.addWidget(z0_lbl, 5,0)
        grid.addWidget(t0_lbl, 6,0)
        grid.addWidget(dots_num_lbl, 7,0)
        grid.addWidget(time_lbl, 8,0)


        grid.addWidget(dxt_field, 0,1)
        grid.addWidget(dyt_field, 1,1)
        grid.addWidget(dzt_field, 2,1)
        grid.addWidget(x0_field, 3,1)
        grid.addWidget(y0_field, 4,1)
        grid.addWidget(z0_field, 5,1)
        grid.addWidget(t0_field, 6,1)
        grid.addWidget(dots_num_field, 7,1)
        grid.addWidget(time_field, 8,1)

        grid.addWidget(draw_btn, 9,1)

        grid.addWidget(toolbar, 10,0)


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
            
    def my_evaluate(self,f,g,k,x0,y0,z0,t0,n,delta_t):
        x,y,z,t = symbols('x y z t')
        
        dots_x = [x0]
        dots_y = [y0]
        dots_z = [z0]
        current_t = t0

        k1,k2,k3,k4 = None, None, None, None
        m1,m2,m3,m4 = None, None, None, None
        j1,j2,j3,j4 = None, None, None, None

        for i in range(1,n+1):
            k1 = f.evalf(subs={x: dots_x[i-1], y: dots_y[i-1], z: dots_z[i-1], t:current_t})*delta_t
            m1 = g.evalf(subs={x: dots_x[i-1], y: dots_y[i-1], z: dots_z[i-1], t:current_t})*delta_t
            j1 = k.evalf(subs={x: dots_x[i-1], y: dots_y[i-1], z: dots_z[i-1], t:current_t})*delta_t

            k2 = f.evalf(subs={x: dots_x[i-1]+k1/2, y: dots_y[i-1]+m1/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            m2 = g.evalf(subs={x: dots_x[i-1]+k1/2, y: dots_y[i-1]+m1/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            j2 = k.evalf(subs={x: dots_x[i-1]+k1/2, y: dots_y[i-1]+m1/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t

            k3 = f.evalf(subs={x: dots_x[i-1]+k2/2, y: dots_y[i-1]+m2/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            m3 = g.evalf(subs={x: dots_x[i-1]+k2/2, y: dots_y[i-1]+m2/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            j3 = k.evalf(subs={x: dots_x[i-1]+k2/2, y: dots_y[i-1]+m2/2, z: dots_z[i-1]+j2/2, t:current_t+delta_t/2})*delta_t

            k4 = f.evalf(subs={x: dots_x[i-1]+k3/2, y: dots_y[i-1]+m3/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            m4 = g.evalf(subs={x: dots_x[i-1]+k3/2, y: dots_y[i-1]+m3/2, z: dots_z[i-1]+j1/2, t:current_t+delta_t/2})*delta_t
            j4 = k.evalf(subs={x: dots_x[i-1]+k3/2, y: dots_y[i-1]+m3/2, z: dots_z[i-1]+j3/2, t:current_t+delta_t/2})*delta_t

            dots_x.append(dots_x[i-1]+(1/6)*(k1+2*k2+2*k3+k4))
            dots_y.append(dots_y[i-1]+(1/6)*(m1+2*m2+2*m3+m4))
            dots_z.append(dots_z[i-1]+(1/6)*(j1+2*j2+2*j3+j4))
            current_t += delta_t

        dots_x = tuple(map(float, dots_x))
        dots_y = tuple(map(float, dots_y))
        dots_z = tuple(map(float, dots_z))
        
        return (dots_x,dots_y,dots_z)
        
        
          
    def buttonClicked(self):
        x,y,z,t = symbols('x y z t')

        f = eval(self.findChild(QLineEdit, "dxt_field").text())
        g = eval(self.findChild(QLineEdit, "dyt_field").text())
        k = eval(self.findChild(QLineEdit, "dzt_field").text())

        n = int(self.findChild(QLineEdit, "dots_num_field").text())
        delta_t = eval(self.findChild(QLineEdit, "time_field").text())

        t0 = eval(self.findChild(QLineEdit, "t0_field").text())
        x0 = eval(self.findChild(QLineEdit, "x0_field").text())
        y0 = eval(self.findChild(QLineEdit, "y0_field").text())
        z0 = eval(self.findChild(QLineEdit, "z0_field").text())

        if not self.isiterable(x0) and not self.isiterable(y0) and not self.isiterable(t0) and not self.isiterable(z0):
            data = self.my_evaluate(f,g,k,x0,y0,z0,t0,n,delta_t)
        else:
            data = [(self.my_evaluate(f,g,k,i,j,q,l,n,delta_t)[0], self.my_evaluate(f,g,k,i,j,q,l,n,delta_t)[1], self.my_evaluate(f,g,k,i,j,q,l,n,delta_t)[2]) for i,j,q,l in zip(x0,y0,z0,t0)]

            
        plt.switch_backend(u"qt5agg")
        ax = plt.axes(projection="3d")
        
        if not self.isiterable(data[0][0]):
            ax.scatter(data[0],data[1],data[2],c='r',s=1)
        else:
            for (i,j,k) in data:
               ax.scatter(i,j,k,c='r', s=1)

        
        #.plot3D(dots_x, dots_y, dots_z, c='red')
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = custom3DEq()
    sys.exit(app.exec_())
