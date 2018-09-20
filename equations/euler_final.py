from matplotlib import pyplot as plt


beg_cond = eval(input("Введите начальные условия в формате x0, y0: "))

delta = eval(input("Введите значение параметра delta: "))

x = [beg_cond[0]]
y = [beg_cond[1]]

n = int(input("Введите количество точек: "))
delta_t = eval(input("Введите 'шаг' времени: "))

current_x = None
current_y = None

for i in range(1,n+1):
    current_x = x[i-1]+delta_t*y[i-1]
    current_y = y[i-1]+delta_t*(-delta*y[i-1]+(1/2)*x[i-1]*(1-(x[i-1])**2))
    x.append(current_x)
    y.append(current_y)

print (map(lambda x: (x[0],x[1]), zip(x,y)))

plt.scatter(x,y,s=3, c='g', marker='o')
plt.xlabel('x')
plt.ylabel('y')
plt.title(u"Решение уравнения Дуффинга методом ломаных Эйлера")
plt.savefig('plot.png')
plt.grid()
plt.show()
