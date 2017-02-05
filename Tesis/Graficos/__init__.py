import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import pyplot
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import sympy as sym
from sympy import *
from datetime import datetime
#nuevo
from mpl_toolkits.mplot3d import Axes3D
import random
import mpl_toolkits.mplot3d.axes3d as axes3d

class Grafico:
    def estilo1(self):
        labelfont = {
            'family' : 'sans-serif',  # (cursive, fantasy, monospace, serif)
            'color'  : 'black',       # html hex or colour name
            'weight' : 'normal',      # (normal, bold, bolder, lighter)
            'size'   : 14,            # default value:12
        }
        titlefont = {
            'family' : 'serif',
            'color'  : 'black',
            'weight' : 'bold',
            'size'   : 16,
        }
        return {'labelfont':labelfont, 'titlefont':titlefont}

    def graficar_funcion(self, expr, str_expr, inferior, superior, estilo):
        x = sym.symbols('x')
        inf = float(sympify(inferior))
        sup = float(sympify(superior))

        xi = np.linspace(inf-1, sup+1, 100)
        xj =  np.linspace(inf, sup, 100)
        Fx = sym.lambdify(x,expr,'numpy')   # Function handle can now take numpy array inputs

        plt.plot(xi, Fx(xi),
            '#638CB5',                # colour
            linestyle='-',              # line style
            linewidth=2-5,                # line width
            label= str_expr )           # plot label

        axes = plt.gca()
        axes.set_xlim([inf-1, sup+1])                           # x-axis bounds
        axes.set_ylim([np.min(Fx(xi))-1,np.max(Fx(xi))+1])      # y-axis bounds

        plt.legend(loc='upper right', shadow=True, fontsize='small')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        #plt.title('Funciones Trigonometricas', fontdict=titlefont)
        plt.xlabel('x', fontdict=labelfont)
        plt.ylabel('f(x)', fontdict=labelfont)

        plt.fill_between(xj,Fx(xj),0,facecolor='0.9', edgecolor='0.5')

        plt.grid()                            # Le agrega la grilla
        #plt.show()

        filename = 'foo-%s.png'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/'+filename
        plt.savefig(filename1, bbox_inches='tight')
        plt.close()
        return filename

    def graficar_biseccion(self, expr, str_expr, inferior, superior, estilo, error):
        x = sym.symbols('x')
        inf = float(sympify(inferior))
        sup = float(sympify(superior))

        xi = np.linspace(inf-.2, sup+.2, 100)
        Fx = sym.lambdify(x,expr,'numpy')   # Function handle can now take numpy array inputs
        fa = Fx(inf)
        fb = Fx(sup)
        if (fa*fb) >= 0:
            return {'error':1, 'band':0}
        else:
            plt.plot(xi, Fx(xi),
                '#638CB5',                # colour
                linestyle='-',              # line style
                linewidth=2-5,                # line width
                label= str_expr )           # plot label

            plt.plot([inf, inf], [Fx(inf),np.min(Fx(xi))-1], color='green', linewidth=1, linestyle="--")
            plt.plot([inf, inf-1], [Fx(inf), Fx(inf)], color='green', linewidth=1, linestyle="--")
            plt.scatter([inf, ], [Fx(inf), ], 50, color='green')
            plt.annotate(r'$(a,f(a))$',xy=(inf, Fx(inf)), xycoords='data',
                 xytext=(7, 0), textcoords='offset points', fontsize=16)

            plt.plot([sup, sup], [Fx(sup),np.min(Fx(xi))-1], color='pink', linewidth=2, linestyle="--")
            plt.plot([sup, inf-1], [Fx(sup), Fx(sup)], color='pink', linewidth=2, linestyle="--")
            plt.scatter([sup, ], [Fx(sup), ], 50, color='pink')
            plt.annotate(r'$(b,f(b))$',xy=(sup, Fx(sup)), xycoords='data',
                 xytext=(7, 0), textcoords='offset points', fontsize=16)

            r = (inf+sup)/2
            plt.plot([r, r], [Fx(r),np.min(Fx(xi))-1], color='orange', linewidth=2, linestyle="--")
            plt.plot([r, inf-1], [Fx(r), Fx(r)], color='orange', linewidth=2, linestyle="--")
            plt.scatter([r, ], [Fx(r), ], 50, color='orange')
            plt.annotate(r'$(r,f(r))$',xy=(r, Fx(r)), xycoords='data',
                xytext=(7, 0), textcoords='offset points', fontsize=16)

            axes = plt.gca()
            axes.set_xlim([inf-.2, sup+.2])                           # x-axis bounds
            axes.set_ylim([np.min(Fx(xi))-.2,np.max(Fx(xi))+.2])      # y-axis bounds

            plt.legend(loc='upper right', shadow=True, fontsize='small')
            labelfont = estilo['labelfont']
            titlefont = estilo['titlefont']
            plt.xlabel('x', fontdict=labelfont)
            plt.ylabel('f(x)', fontdict=labelfont)
            plt.grid()                            # Le agrega la grilla
            #plt.show()

            filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
            filename1 = 'Tesis/static/imagenes/'+filename

            plt.savefig(filename1, bbox_inches='tight')
            axes.cla()
            plt.clf()
            plt.close()

            #algoritmo
            band = 0;
            r = (inf+sup)/2
            fr = Fx(r)

            if (abs(inf-sup) <= float(error)) or (abs(fr) <= float(error)):
            #if (abs(inf-sup) <= float(error)):
                band = 1
            else:
                fa = Fx(inf)
                fb = Fx(sup)
            #Fin algoritmo
            return {'filename':filename, 'inf':inf, 'sup':sup, 'fa':fa, 'fb':fb, 'raiz':r, 'fr':fr, 'band':band, 'error':0}

    def agregarEjes(self):
        plt.subplots_adjust(left=0.15)        # prevents overlapping of the y label
        plt.axhline(y=0, color='gray')
        plt.axvline(x=0, color='gray')


    def graficar_derivada(self, expr, str_expr, x0, xn, estilo, derivada, variable):
        x = sym.symbols('x')
        inf = float(sympify(x0))
        sup = float(sympify(xn))
        print "expr "+str_expr
        print "derivada "+str(derivada)
        xi = np.linspace(inf, sup, 100)
        #Fx = sym.lambdify(x,expr,'numpy')   # Function handle can now take numpy array inputs
        Fx = np.vectorize(sym.lambdify(x, expr, "numpy"))
        Fx2 = np.vectorize(sym.lambdify(x, derivada, "numpy"))
        str1 = 'f('+str(variable)+') = '+str(str_expr)
        str2 = 'f\'(x) = '+str(derivada)
        plt.plot(xi, Fx(xi),
            '#638CB5',
            linestyle='-',
            linewidth=2-5,
            label= str1 )

        plt.plot(xi, Fx2(xi),
            'red',
            linestyle='-',
            linewidth=2-5,
            label= str2 )

        axes = plt.gca()
        #axes.autoscale()
        axes.set_xlim([inf, sup])                           # x-axis bounds
        minimo = min(np.min(Fx(xi))-1,np.min(Fx2(xi))-1)
        maximo = max(np.max(Fx(xi))+1,np.max(Fx2(xi))+1)
        axes.set_ylim([minimo,maximo])      # y-axis bounds

        plt.legend(loc='upper right', shadow=True, fontsize='medium')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        #plt.title('Funciones Trigonometricas', fontdict=titlefont)
        plt.xlabel('x', fontdict=labelfont)
        plt.ylabel('f(x)', fontdict=labelfont)
        plt.grid()                            # Le agrega la grilla
        #plt.show()

        filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/'+filename
        plt.savefig(filename1, bbox_inches='tight')
        plt.close()
        return {'filename':filename, 'funcion':str_expr, 'derivada': str(derivada)}

    def fun(x, y):
        return x**2+y

    def graficar_funcion1(self, expr, str_expr, inferior, superior, inferior1, superior1, estilo):
        inf = float(sympify(inferior))
        sup = float(sympify(superior))
        inf1 = float(sympify(inferior1))
        sup1 = float(sympify(superior1))
        x = sym.symbols('x')
        y = sym.symbols('y')
        fun = sym.lambdify((x,y),expr,'numpy')

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = np.arange(inf-1, sup+1, 0.04)
        y = np.arange(inf1-1, sup1+1, 0.04)
        X, Y = np.meshgrid(x, y)
        zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)

        ax.plot_surface(X, Y, Z,
        cmap=cm.summer)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/'+filename
        plt.savefig(filename1, bbox_inches='tight')
        plt.close()
        return filename
