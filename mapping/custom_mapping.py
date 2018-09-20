from sympy import *
from matplotlib import pyplot as plt
import itertools


x,y = symbols("x y")
f = eval(input("x = "))
g = eval(input("y = "))

x0,y0 = eval(input("Введите начальную точку: "))
n = int(input("Введите кол-во итераций: "))

xs = [x0]
ys = [y0]

for i in range(1,n+1):
    xs.append(f.evalf(subs={x: xs[i-1], y: ys[i-1]}))
    ys.append(g.evalf(subs={x: xs[i-1], y: ys[i-1]}))

plt.scatter(xs,ys, s=1, c='green')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('mapping.png')
plt.grid()
plt.show()
