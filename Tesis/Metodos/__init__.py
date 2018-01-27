from sympy import *
import sympy as sym
import numpy as np
import sys


class Metodos:

    def trapecio2D(self, funcion, variable1, variable2, a, b, c, d, m, n):
        h = (b-a)/m
        k = (d-c)/n
        x, y, z = symbols('x y z')
        fun = sym.lambdify((x,y),funcion,'numpy')
        #variable es cual de las dos se modifica (1 y 2 corresponden a x e y)
        def sumatoria (fin,x,y,variable):
            resultado = 0
            if (variable ==1):
                for i in xrange(1,fin):
                    resultado = resultado + fun(a+i*h,y)
            else:
                for j in xrange(1,fin):
                    resultado = resultado + fun(x,c+j*k)
            return resultado

        def sumatoriaDoble(m,n):
            resultado = 0
            for j in xrange (1,n):
                for i in xrange (1,m):
                    resultado = resultado + fun((a+i*h),(c+j*k))
            return resultado

        sumaPuntos = fun(a,c)+fun(b,c)+fun(a,d)+fun(b,d)
        td2 = float(1)/float(4)*h*k*(sumaPuntos+2*sumatoria(m,x,c,1)+2*sumatoria(m,x,d,1)+2*sumatoria(n,a,y,2)+2*sumatoria(n,b,y,2)+
        4*sumatoriaDoble(m,n))
        print td2
        return {'aproximacion': td2}

    def simpson2D(self, funcion, variable1, variable2, a, b, c, d, m, n):
        h = (b-a)/(2*m)
        k = (d-c)/(2*n)
        x, y, z = symbols('x y z')
        fun = sym.lambdify((x,y),funcion,'numpy')

        #variable es cual de las dos se modifica (1 y 2 corresponden a x e y)
        def sumatoria (fin,x,y,variable,par):
            resultado = 0
            if (variable == 1):
                for i in xrange(1,fin):
                    if (par == true):
                        resultado = resultado + fun(a+h*2*i,y)
                    else:          
                        resultado = resultado + fun(a+h*(2*i-1),y)
            else:
                for j in xrange(1,fin):
                    if (par == true):
                        resultado = resultado + fun(x, c+k*2*j)
                    else:
                        resultado = resultado + fun(x, c+k*(2*j-1))
            return resultado

        def sumatoriaDoble(m,n,pari,parj):
            resultado = 0
            for j in xrange (1,n):
                for i in xrange (1,m):
                    if (pari == true):
                        if (parj == true):
                            resultado = resultado + fun((a+h*2*i),(c+k*2*j))
                        else:
                            resultado = resultado + fun((a+h*2*i),(c+k*(2*j-1)))
                    else:
                        if (parj == true):
                            resultado = resultado + fun((a+h*(2*i-1)),(c+k*2*j))
                        else:
                            resultado = resultado + fun((a+h*(2*i-1)),(c+k*(2*j-1)))
            return resultado

        sumaPuntos = fun(a,c)+fun(b,c)+fun(a,d)+fun(b,d)
        print 'sumatoria'
        print sumatoriaDoble(m,n,true,true)

        sd2 = float(1)/float(9)*h*k*(sumaPuntos+4*sumatoria(n+1,a,y,2,false)
        +2*sumatoria(n,a,y,2,true)+4*sumatoria(n+1,b,y,2,false)+2*sumatoria(n,b,y,2,true)
        +4*sumatoria(m+1,x,c,1,false)+4*sumatoria(m+1,x,d,1,false)+2*sumatoria(m,x,c,1,true)
        +2*sumatoria(m,x,d,1,true)+16*sumatoriaDoble(m+1,n+1,false,false)+8*sumatoriaDoble(m+1,n,false,true)
        +8*sumatoriaDoble(m,n+1,true,false)+4*sumatoriaDoble(m,n,true,true))
        print sd2
        return {'aproximacion': sd2}
