from matplotlib import pyplot as plt

beg_cond = eval(input("Введите начальные условия в формате x0, y0: "))

delta = eval(input("Введите значение параметра delta: "))

x = [beg_cond[0]]
y = [beg_cond[1]]

n = int(input("Введите количество точек: "))
delta_t = eval(input("Введите 'шаг' времени: "))

current_x = None
current_y = None
k1,k2,k3,k4,m1,m2,m3,m4 = None,None,None,None,None,None,None,None,

for i in range(1,n+1):
    k1 = y[i-1]*delta_t
    m1 = (-delta*y[i-1] + (1/2)*x[i-1]*(1-(x[i-1])**2))*delta_t

    k2 = (y[i-1] + m1/2) * delta_t
    m2 = (-delta*(y[i-1]+m1/2) + (1/2)*(x[i-1]+k1/2)*(1-(x[i-1]+k1/2)**2))*delta_t

    k3 = (y[i-1] + m2/2) * delta_t
    m3 = (-delta*(y[i-1]+m2/2) + (1/2)*(x[i-1]+k2/2)*(1-(x[i-1]+k2/2)**2))*delta_t

    k4 = (y[i-1] + m3/2) * delta_t
    m4 = (-delta*(y[i-1]+m3/2) + (1/2)*(x[i-1]+k3/2)*(1-(x[i-1]+k3/2)**2))*delta_t

    x.append(x[i-1]+(1/6)*(k1+2*k2+2*k3+k4))
    y.append(y[i-1]+(1/6)*(m1+2*m2+2*m3+m4))

# print (list(map(lambda x: (x[0],x[1]), zip(x,y))))

plt.scatter(x,y,s=3, c='r', marker='o')
plt.xlabel('x')
plt.ylabel('y')
plt.title(u"Решение уравнения Дуффинга методом Рунге-Кутты")
plt.savefig('plot.png')
plt.grid()
plt.show()
