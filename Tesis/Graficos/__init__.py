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
from mpl_toolkits.mplot3d import Axes3D
import random
import mpl_toolkits.mplot3d.axes3d as axes3d


class Grafico:

    def estilo1(self):
        labelfont = {
            'family': 'sans-serif',  # (cursive, fantasy, monospace, serif)
            'color': 'black',       # html hex or colour name
            'weight': 'normal',      # (normal, bold, bolder, lighter)
            'size': 14,            # default value:12
        }
        titlefont = {
            'family': 'serif',
            'color': 'black',
            'weight': 'bold',
            'size': 16,
        }
        return {'labelfont': labelfont, 'titlefont': titlefont}

    def graficarFuncion(self, expr, str_expr, variable, inferior, superior, estilo, sombra):
        x = sym.symbols(variable)
        inf = float(sympify(inferior))
        sup = float(sympify(superior))

        if int(sombra) == 1:
            xi = np.linspace(inf - 1, sup + 1, 100)
        else:
            xi = np.linspace(inf, sup, 100)
        xj = np.linspace(inf, sup, 100)
        # Function handle can now take numpy array inputs
        Fx = sym.lambdify(x, expr, 'numpy')

        plt.plot(xi, Fx(xi),
            '#638CB5',                # colour
            linestyle='-',              # line style
            linewidth=2 - 5,                # line width
            label= 'f('+variable+') = '+str_expr)           # plot label

        axes = plt.gca()
        # x-axis bounds
        # Si es para el grafico de la funcion debajo de la curva, le agrego 1 a los limites 
        if int(sombra) == 1:
            axes.set_xlim([inf - 1, sup + 1])
            axes.set_ylim([np.min(Fx(xi)) - 1, np.max(Fx(xi)) + 1])      # y-axis bounds
        # En los otros casos grafico hasta los limites ingresado
        else:
            axes.set_xlim([inf, sup])
            axes.set_ylim([np.min(Fx(xi)), np.max(Fx(xi))])      # y-axis bounds

        plt.legend(loc='upper right', shadow=True, fontsize='small')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        # plt.title('Funciones Trigonometricas', fontdict=titlefont)
        plt.xlabel(variable, fontdict=labelfont)
        plt.ylabel('f('+variable+')', fontdict=labelfont)
        if int(sombra) == 1:
            plt.fill_between(xj, Fx(xj), 0, facecolor='0.9', edgecolor='0.5')

        plt.grid()                            # Le agrega la grilla

        filename = 'foo-%s.png' % datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/' + filename
        plt.savefig(filename1, bbox_inches='tight')
        plt.close()
        return filename

    def graficar_biseccion(self, expr, str_expr, inferior, superior, estilo, error):
        x = sym.symbols('x')
        inf = float(sympify(inferior))
        sup = float(sympify(superior))
        axes = plt.gca()
        
        ls = np.linspace(inf, sup, 100)
        #calculo cuanto dejo en los extremos a partir despues de inf y sup
        calc = (ls[10] - ls[0])/2
        xi = np.linspace(inf-calc, sup+calc, 100)

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
                label= 'f(x) = '+str_expr )           # plot label
            
            axes.set_xlim([inf-calc, sup+calc])                           # x-axis bounds
            axes.set_ylim(auto=True) 
            
            # Graficar punto inferior
            plt.scatter([inf, ], [Fx(inf), ], 50, color='green')
            plt.annotate(r'$(a,f(a))$',xy=(inf, Fx(inf)), xycoords='data',
                 xytext=(7, 0), textcoords='offset points', fontsize=16)
            
            # Graficar punto superior
            plt.scatter([sup, ], [Fx(sup), ], 50, color='red')
            plt.annotate(r'$(b,f(b))$',xy=(sup, Fx(sup)), xycoords='data',
                 xytext=(7, 0), textcoords='offset points', fontsize=16)

            # Calcula raiz y dibuja el punto
            r = (inf+sup)/2
            plt.scatter([r, ], [Fx(r), ], 50, color='orange')
            plt.annotate(r'$(r,f(r))$',xy=(r, Fx(r)), xycoords='data',
                xytext=(7, 0), textcoords='offset points', fontsize=16)

            # Lineas de (a, fa)
            plt.plot([inf,inf-calc], [Fx(inf),Fx(inf)], color='green', linewidth=1)
            plt.plot([inf,inf], [Fx(inf),0], color='green', linewidth=1)

            # Lineas de (b, fb)
            plt.plot([sup, sup], [Fx(sup),0], color='red', linewidth=1)
            plt.plot([sup, inf-calc], [Fx(sup), Fx(sup)], color='red', linewidth=1)
            
            # Lineas de (r, fr)
            plt.plot([r, r], [Fx(r),0], color='orange', linewidth=1)
            plt.plot([r, inf-calc], [Fx(r), Fx(r)], color='orange', linewidth=1)

            plt.legend(loc='upper right', shadow=True, fontsize='small')
            labelfont = estilo['labelfont']
            titlefont = estilo['titlefont']
            plt.xlabel('x', fontdict=labelfont)
            plt.ylabel('f(x)', fontdict=labelfont)
            plt.grid()                            # Le agrega la grilla

            filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
            filename1 = 'Tesis/static/imagenes/'+filename

            plt.savefig(filename1, bbox_inches='tight')
            plt.clf()
            plt.close()

            # algoritmo de biseccion
            
            band = 0;
            r = (inf+sup)/2
            fr = Fx(r)

            if (abs(inf-sup) <= float(error)) or (abs(fr) <= float(error)):
                band = 1
            else:
                fa = Fx(inf)
                fb = Fx(sup)
            
            # Fin algoritmo
     
            #round a 5 solo si tienen mas de 5 decimales
            if (str(fa)[::-1].find('.') > 5):
                fa = fa.round(5)

            if (str(fb)[::-1].find('.') > 5):
                fb= fb.round(5)

            if (str(fr)[::-1].find('.') > 5):
                fr= fr.round(5)

            return {'filename':filename, 'inf':inf, 'sup':sup, 'fa':fa, 'fb':fb, 'raiz':r, 'fr':fr, 'band':band, 'error':0}
            

    def graficar_newton(self, expr, str_expr, x0, derivada, estilo, error):
        x = sym.symbols('x')
        varx0 = float(sympify(x0))
        dFx = sym.lambdify(x,derivada,'numpy')
        dfx0 = dFx(varx0)
        axes = plt.gca()
        Fx = sym.lambdify(x,expr,'numpy')   # Function handle can now take numpy array inputs
        fx0 = Fx(varx0)
        x1 = varx0-(fx0/dfx0)
        
        ls = np.linspace(varx0, x1, 100)
        calc = (ls[10] - ls[0])/2
        xi = np.linspace(varx0-calc, x1+calc, 100)

        plt.plot(xi, Fx(xi),
            '#638CB5',                # colour
            linestyle='-',              # line style
            linewidth=2-5,                # line width
            label= str_expr )           # plot label

         # x-axis bounds
        if (varx0 < x1):
            axes.set_xlim([varx0-calc, x1+calc])
            liminf = varx0-calc
            limsup = x1+calc
        else:
            axes.set_xlim([x1+calc, varx0-calc])
            liminf = x1+calc
            limsup = varx0-calc
        # y-axis bounds
        axes.set_ylim(auto=True) 
        
        # Graficar punto x0
        plt.scatter([varx0, ], [Fx(varx0), ], 50, color='green')
        plt.annotate(r'$(x0,f(x0))$',xy=(varx0, Fx(varx0)), xycoords='data',
                xytext=(7, 0), textcoords='offset points', fontsize=16)

        # Graficar punto x1
        plt.scatter([x1, ], [Fx(x1), ], 50, color='orange')
        plt.annotate(r'$(x1,f(x1))$',xy=(x1, Fx(x1)), xycoords='data',
            xytext=(7, 0), textcoords='offset points', fontsize=16)
                
        # Lineas de (x0, f(x0))
        plt.plot([varx0, liminf], [Fx(varx0),Fx(varx0)], color='green', linewidth=1)
        plt.plot([varx0, varx0], [Fx(varx0), 0], color='green', linewidth=1)

        # Lineas de (x1, f(x1))

        plt.plot([x1, x1], [Fx(x1),0], color='orange', linewidth=1)
        plt.plot([x1, liminf], [Fx(x1), Fx(x1)], color='orange', linewidth=1)


        plt.legend(loc='upper right', shadow=True, fontsize='small')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        plt.xlabel('x', fontdict=labelfont)
        plt.ylabel('f(x)', fontdict=labelfont)
        plt.grid()                            # Le agrega la grilla
        # plt.show()

        filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/'+filename

        plt.savefig(filename1, bbox_inches='tight')
        axes.cla()
        plt.clf()
        plt.close()

        # algoritmo
        band = 0;
        x1 = round(varx0-(fx0/dfx0),4)
        fx1 = round(Fx(x1),4)
        x0 = x1

        if (abs(fx1) <= float(error)):
            band = 1
        else:
            x0 = x1
        # Fin algoritmo
        return {'filename':filename, 'x0':x0, 'fx0':round(fx0,4), 'x1': x1, 'fx1':fx1, 'band':band, 'error':0}

    def agregarEjes(self):
        plt.subplots_adjust(left=0.15)        # prevents overlapping of the y label
        plt.axhline(y=0, color='gray')
        plt.axvline(x=0, color='gray')


    def graficar_derivada(self, expr, str_expr, x0, xn, estilo, derivada, variable):
        x = sym.symbols('x')
        inf = float(sympify(x0))
        sup = float(sympify(xn))
        xi = np.linspace(inf, sup, 100)
        # Fx = sym.lambdify(x,expr,'numpy')   # Function handle can now take numpy array inputs
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
        # axes.autoscale()
        axes.set_xlim([inf, sup])                           # x-axis bounds
        minimo = min(np.min(Fx(xi))-1,np.min(Fx2(xi))-1)
        maximo = max(np.max(Fx(xi))+1,np.max(Fx2(xi))+1)
        axes.set_ylim([minimo,maximo])      # y-axis bounds
        plt.legend(loc='upper right', shadow=True, fontsize='medium')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        # plt.title('Funciones Trigonometricas', fontdict=titlefont)
        plt.xlabel('x', fontdict=labelfont)
        plt.ylabel('f(x)', fontdict=labelfont)
        plt.grid()                            # Le agrega la grilla
        # plt.show()

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

    def funciones(self, inferior, superior, estilo, variable, funciones):
        x = sym.symbols('x')
        inferior = float(sympify(inferior))
        superior = float(sympify(superior))
        xi = np.linspace(inferior, superior, 100)
        colores = ['#638CB5', 'red', 'green', '#FF8000', '#BF00FF']
        for i in xrange(0, 5):
            funcion = funciones[i]
            if (i>0):
                min_anterior = np.min(Fx(xi))-1
                max_anterior = np.max(Fx(xi))+1
            else:
                min_anterior = 0
                max_anterior = 0
                
            if str(funcion) != '':
                Fx = np.vectorize(sym.lambdify(x, funcion, "numpy"))
                minimo = min(np.min(Fx(xi))-1, min_anterior)
                maximo = max(np.max(Fx(xi))+1, max_anterior)
                
                label = 'f'+str(i+1)+'('+str(variable)+') = '+str(funcion)
                plt.plot(xi, Fx(xi),
                # '#638CB5',
                colores[i],
                linestyle='-',
                linewidth=2-4,
                label= label )

        axes = plt.gca()
        # axes.set_xlim([inferior, superior])                           # x-axis bounds
        axes.set_xlim(auto=True)                          # x-axis bounds
        
        # minimo = min(np.min(Fx(xi))-1,np.min(Fx2(xi))-1)
        # maximo = max(np.max(Fx(xi))+1,np.max(Fx2(xi))+1)
        # axes.set_ylim([minimo,maximo])      # y-axis bounds
        
        # axes.set_ylim([-10,10])      # y-axis bounds
        axes.set_ylim(auto=True)      # y-axis bounds
        
        plt.legend(loc='upper right', shadow=True, fontsize='small')
        labelfont = estilo['labelfont']
        titlefont = estilo['titlefont']
        plt.xlabel('x', fontdict=labelfont)
        plt.grid()                            # Le agrega la grilla

        filename = 'foo-%s.jpeg'%datetime.now().strftime('%Y-%m-%d_%H%M%S')
        filename1 = 'Tesis/static/imagenes/'+filename
        plt.savefig(filename1, bbox_inches='tight')
        plt.close()
        return {'filename':filename}
        