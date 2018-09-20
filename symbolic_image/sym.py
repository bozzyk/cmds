from sympy import *
import numpy as np
import winsound
from pprint import pprint as p
import networkx as nx
import time, terminal_size
from console_progressbar import ProgressBar



#--------------------------------HENON------------------------------------------
# x = 1 - a*x**2 + y    |  x = 1 - 1.4*x**2 + y
# y = b*x              |   y = 0.3*x
#-------------------------------------TABLE-------------------------------------
# @njit
class Table:
    struct = None
    contours = None
    images = None
    symbolic_image = None
    eps = 0

    # @void(float_,float_,float_,float_,float_,float_,float_)
    def __init__(self,a,b,c,d,diam_x,diam_y,eps):
        struct = {}
        counter = 1
        for i in range(int((b-a)/diam_x)):
            for j in range(int((d-c)/diam_y)):
                # returns [(xi,xi+1),(yi,yi+1)]
                struct[str(counter)] = [(a+diam_x*i,a+diam_x*(i+1)), (c+diam_y*j, c+diam_y*(j+1))]
                counter += 1
        self.struct = struct
        self.eps = eps
        self.borders = [a,b,c,d]


    def union(self, t2):
        tmp = {}
        j = 1
        num = len(self.struct) + len(t2.struct)
        for i in range(1,num+1):
            if i <= len(self.struct):
                tmp[str(i)] = self.struct[str(i)]
            else:
                tmp[str(i)] = t2.struct[str(j)]
                j += 1

        self.struct = tmp
        return

    def section_divide(self, coords_beg, coords_end, n):
        x0,y0 = coords_beg
        x1,y1 = coords_end

        x_step = (x1-x0)/n
        y_step = (y1-y0)/n

        x_dots = [x0 + x_step*i for i in range(1,n)]
        y_dots = [y0 + y_step*i for i in range(1,n)]

        return list(zip(x_dots, y_dots))

    # @void (float_)
    def get_cells_contours(self, precision):
        pb = ProgressBar(total=100,decimals = 2,prefix="getting cells contours", length = terminal_size.get_terminal_size()[0]-40,fill='#',zfill='-')
        contours = {}
        l = 1
        step = 100/len(self.struct)
        for i in self.struct.values():

            x0,x1 = i[0][0],i[0][1]
            y0,y1 = i[1][0], i[1][1]

            bottom_dots = self.section_divide((x0,y0), (x1,y0), precision)
            right_dots = self.section_divide((x1,y0), (x1,y1), precision)
            top_dots = self.section_divide((x1,y1), (x0,y1), precision)
            left_dots = self.section_divide((x0,y1), (x0,y0), precision)

            inner_dots = []
            for k in bottom_dots:
                for j in left_dots:
                    inner_dots.append((k[0],j[1]))

            contours[str(l)] = [(x0,y0)] + bottom_dots + [(x1,y0)] + right_dots + [(x1,y1)] + top_dots + [(x0,y1)] + left_dots + inner_dots


            pb.print_progress_bar(step*l)

            l += 1
        self.contours = contours


    def get_cells_images(self, f, g): #f,g - lambdified functions of x,y
        pb = ProgressBar(total=100,decimals = 2,prefix="getting cells images", length = terminal_size.get_terminal_size()[0]-40,fill='#',zfill='-')
        images = {}
        j = 1
        step = 100/len(self.contours)
        for i in self.contours.values():
            images[str(j)] =  list(map(lambda x: (f(x[0],x[1]), g(x[0],x[1])), i))
            pb.print_progress_bar(step*j)
            j += 1

        self.images = images

    def dot_in_cell(self,dot,cell):
        # dot: (x,y); cell: [(x0,x1),(y0,y1)]
        # calculate with eps precision
        x0,x1 = cell[0]
        y0,y1 = cell[1]
        dot_x, dot_y = dot
        if x0-self.eps <= dot_x <= x1+self.eps and y0-self.eps <= dot_y <= y1+self.eps:
            return True
        else: return False

    # @void()
    def get_cells_intersects(self):
        pb = ProgressBar(total=100,decimals = 2,prefix="getting cells intersects", length = terminal_size.get_terminal_size()[0]-45,fill='#',zfill='-')
        intersects = {}
        m = 1
        step = 100/(len(self.images)*len(self.images['1']))
        for i in self.images:
            intersects[i] = set()
            for j in self.images[i]:
                for k in self.struct:
                    if self.dot_in_cell(j,self.struct[k]): intersects[i].add(k)
                pb.print_progress_bar(step*m)
                m += 1
        self.intersects = intersects

    # @void()
    def clear_table(self):
        pb = ProgressBar(total=100,decimals = 2,prefix="clearing table", length = terminal_size.get_terminal_size()[0]-40,fill='#',zfill='-')
        connected = tuple(nx.strongly_connected_components(self.symbolic_image))
        remember = set()
        rest = {}
        for i in connected:
            if len(i) > 1:
                remember.update(i)
            # else:
            #     try: nx.find_cycle(self.symbolic_image, i)
            #     except nx.exception.NetworkXNoCycle: pass
            #     else: remember.update(i)


        step = 100/len(self.struct)
        k = 1
        m = 1
        for i in self.struct:
            if i in remember:
                rest[str(k)] = self.struct[i]
                k += 1
            pb.print_progress_bar(m*step)
            m += 1

        self.struct = rest


    def get_symbolic_image(self, precision,f,g):
        self.get_cells_contours(precision)
        self.get_cells_images(f,g)
        self.get_cells_intersects()

        pb = ProgressBar(total=100,decimals = 2,prefix="building graph", length = terminal_size.get_terminal_size()[0]-45,fill='#',zfill='-')
        step = 50/len(self.struct)
        m = 1
        G = nx.DiGraph()
        for i in self.struct:
            G.add_node(i)
            pb.print_progress_bar(m*step)
            m += 1

        step = 50/len(self.intersects)
        m = 1
        for i in self.intersects:
            for j in self.intersects[i]: G.add_edge(i,j)
            pb.print_progress_bar(m*step)
            m += 1

        self.symbolic_image = G
        self.clear_table()


    # @void(float_,float_)
    def divide_cells(self, n_x, n_y): #divides cell on n_x*n_y parts
        new_tables = []
        for i in self.struct:
            x0,x1 = self.struct[i][0]
            y0,y1 = self.struct[i][1]
            new_tables.append(Table(x0,x1,y0,y1, (x1-x0)/n_x, (y1-y0)/n_y, self.eps))

        t = new_tables[0]
        for i in new_tables[1:]: t.union(i)
        self.struct = t.struct

    def iterate_proc(self, n_x, n_y, *args): #n_x, n_y, precision, f, g
        self.get_symbolic_image(*args)
        self.divide_cells(n_x, n_y)


    def draw_table(self, save=True, name='figure', interactive=True):
        import matplotlib
        from matplotlib.patches import Polygon
        from matplotlib.collections import PatchCollection
        import matplotlib.pyplot as plt

        patches = []
        fig = plt.subplot()

        for i in self.struct:
            x0,x1 = self.struct[i][0]
            y0,y1 = self.struct[i][1]
            dots = np.array([np.array((x0,y0)),np.array((x1,y0)),np.array((x1,y1)),np.array((x0,y1))])
            polygon = Polygon(dots, True)
            patches.append(polygon)

        p = PatchCollection(patches, alpha=0.7)
        p.set_edgecolor('#000000')
        p.set_facecolor("#FF0d10")
        fig.axis(self.borders)
        fig.add_collection(p)

        if save:
            plt.savefig(name)
            plt.clf()
        if interactive: plt.show()

    def iterates(self, n, save, name, interactive, *args): #args == n_x, n_y, precision, f, g
        begin = time.time()
        for i in range(n):
            self.iterate_proc(*args)
            print ("Iteration time: ", end = " ")
            print (time.time() - begin)
            print ("There are " + str(len(self.struct)) + " cells")
            winsound.PlaySound("notif.mp3", winsound.SND_FILENAME)
            self.draw_table(save, name+str(i), interactive)
            begin = time.time()
#-----------------------------------TABLE_END-----------------------------------

x,y = symbols('x,y')

f = lambdify([x,y], eval(input("f = ")), np)
g = lambdify([x,y], eval(input("g = ")), np)

a,b = eval(input("Enter xmin, xmax: "))
c,d = eval(input("Enter ymin, ymax: "))
diam_x = eval(input("Enter decomposition diameter by x: "))
diam_y = eval(input("Enter decomposition diameter by y: "))
eps = eval(input("Enter cell's image extension: "))
iter_num = eval(input("Enter the number of iterations: "))
save = True if input("Do you want to save the result? (y/n): ")=='y' else False
interactive =  True if input("Do you want to draw the result? (y/n): ")=='y' else False
name = input("Enter the name of pictures to save: ")
split_x = eval(input("Enter the number of subdivision by x: "))
split_y = eval(input("Enter the number of subdivision by y: "))
prec = eval(input("Enter the number of dots on every side of cell's contour (integer): "))

mapping = Table(a,b,c,d,diam_x, diam_y, eps)
mapping.iterates(iter_num, save, name, interactive, split_x, split_y, prec, f,g)
# --------------------------------------------------------------------------------------------------
# t = 0.4 - 6/(1+x**2+y**2)
# vanderpoll_f = lambdify([x,y],y, np)
# vanderpoll_g = lambdify([x,y],4*(1-x**2)*y-x, np)
#
# ikeda_f = lambdify([x,y], 0.6+0.9*(x*cos(t)-y*sin(t)), np)
# ikeda_g = lambdify([x,y], 0.9*(x*sin(t)-y*cos(t)), np)
#
# henon_f = lambdify([x,y], 1 + y - 1.4*x**2, np)
# henon_g = lambdify([x,y], 0.3 * x, np)
#
# henon = Table(-1.5,1.5,-1,1,0.2,0.2,0.000007)
# henon.iterates(6, True, 'henon_final_clear_', False,3,3,3,henon_f,henon_g)

# ikeda =  Table(-1.5,1.5,-2,2,0.1,0.1,0.000007)
# ikeda.iterates(6, True, 'ikeda_final_clear_', False, 3, 3, 3, ikeda_f, ikeda_g)
#
# vanderpoll = Table(-10,10,-10,10,1,1,0.000007)
# vanderpoll.iterates(6, True, 'vanderpoll_final_clear_', False, 3, 3, 3, vanderpoll_f, vanderpoll_g)
