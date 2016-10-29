# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Integrales.formularios import FuncionForm
from Integrales.formularios import FuncionDobleForm
from Integrales.formularios import BiseccionForm
from Integrales.formularios import DerivadaForm
from sympy import *
from django.contrib import messages
from Tesis.Graficos import Grafico
import os, glob

import json
import socket

# Create your views here.

def auxiliar(datos):
    x0, fx0 = datos['x0'], datos['fx0']
    if x0 != "":
        x1, fx1 = datos['x1'], datos['fx1']
        if x1 != "":
            x2, fx2 = datos['x2'], datos['fx2']
            if x2 != "":
                x3, fx3 = datos['x3'], datos['fx3']
                if x3 != "":
                    x4, fx4 = datos['x4'], datos['fx4']
                    if x4 != "":
                        x5, fx5 = datos['x5'], datos['fx5']
                        if x5 != "":
                            ene = 5
                        else:
                            ene, fx5 = 4, '0'
                    else:
                        ene, fx4, fx5 = 3, '0', '0'
                else:
                    ene, fx3, fx4, fx5 = 2, '0', '0', '0'
            else:
                ene, fx2, fx3, fx4, fx5 = 1, '0', '0', '0', '0'
        else:
            ene, fx1, fx2, fx3, fx4, fx5 = 0, '0', '0', '0', '0', '0'
    else:
        ene, fx0, fx1, fx2, fx3, fx4, fx5 = -1, '0', '0', '0', '0', '0', '0'
    return {'ene':ene, 'fx0':fx0, 'fx1':fx1, 'fx2':fx2, 'fx3':fx3, 'fx4':fx4, 'fx5':fx5}

#algo similar para integrales dobles, un método similar a éste
def integrales(request):
    #ver como hago para obtener todos los simbolos de la funcion para declararlos
    x, y, z = symbols('x y z')
    if request.method == 'POST':
        form = FuncionForm(request.POST)
        if form.is_valid():
            str_expr = form.cleaned_data['funcion']
            inferior = form.cleaned_data['inferior']
            superior = form.cleaned_data['superior']
            definida = form.cleaned_data['definida']
            numerica = form.cleaned_data['numerica']
            formula = form.cleaned_data['formula']
            variable = sympify(form.cleaned_data['variable'])
            try:
                expr = sympify(str_expr)
                resu = expr.evalf()
                if 'integrar' in request.POST:
                    #si se va a calcular la integral definida
                    if definida:
                        #Integral definida Numérica
                        if numerica:
                            resu = auxiliar(form.cleaned_data)
                            n = resu['ene']
                            if (n>=1):
                                indice_n = "fx"+str(n)
                                count = 1
                                subtotal = 0
                                #Se va a utilizar el método del trapecio
                                if formula == 'trapecio':
                                    h = (sympify(superior) - sympify(inferior))/(2*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        subtotal = subtotal + sympify(resu[indice])
                                        count += 1
                                    subtotal = 2*subtotal

                                #Se va a utilizar el método de Simpson
                                else:
                                    h = (sympify(superior) - sympify(inferior))/(3*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        if count % 2 == 0:
                                            subtotal = subtotal + (2 * sympify(resu[indice]))
                                        else:
                                            subtotal = subtotal + (4 * sympify(resu[indice]))
                                        count += 1

                                integral = h*(float(resu['fx0'])+float(resu[indice_n])+subtotal)
                                texto = " integral ≈ %1.5f " % integral
                                messages.add_message(request, messages.INFO, texto)
                            else:
                                messages.add_message(request, messages.INFO, 'Se necesitan mas valores para aplicar el método')
                        #integral definida simple
                        else:
                            integralDef = integrate(expr,(variable, inferior, superior))
                            texto = " Integral Definida = %1.5f " % integralDef
                            messages.add_message(request, messages.INFO, texto)
                    #Integral indefinida
                    else:
                        integralInd = integrate(expr,variable)
                        texto = " Integral Indefinida = "+str(integralInd)
                        messages.add_message(request, messages.INFO, texto)
                #else:
                    #messages.add_message(request, messages.SUCCESS, 'Función: '+str_expr)
            except (TypeError, AttributeError, SympifyError):
                messages.add_message(request, messages.INFO, 'Expresión inválida')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FuncionForm()
    return render(request, 'integrales.html', {'form': form})

def integralesDobles(request):
    #ver como hago para obtener todos los simbolos de la funcion para declararlos
    x, y, z = symbols('x y z')
    if request.method == 'POST':
        form = FuncionDobleForm(request.POST)
        if form.is_valid():
            str_expr = form.cleaned_data['funcion']
            inferior = form.cleaned_data['inferior']
            superior = form.cleaned_data['superior']
            inferior1 = form.cleaned_data['inferior1']
            superior1 = form.cleaned_data['superior1']
            definida = form.cleaned_data['definida']
            numerica = form.cleaned_data['numerica']
            formula = form.cleaned_data['formula']
            variable = sympify(form.cleaned_data['variable'])
            variable1 = sympify(form.cleaned_data['variable1'])
            try:
                expr = sympify(str_expr)
                resu = expr.evalf()
                if 'integrar' in request.POST:
                    #si se va a calcular la integral definida
                    if definida:
                        #Integral definida Numérica
                        if numerica:
                            resu = auxiliar(form.cleaned_data)
                            n = resu['ene']
                            if (n>=1):
                                indice_n = "fx"+str(n)
                                count = 1
                                subtotal = 0
                                #Se va a utilizar el método del trapecio
                                if formula == 'trapecio':
                                    h = (sympify(superior) - sympify(inferior))/(2*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        subtotal = subtotal + sympify(resu[indice])
                                        count += 1
                                    subtotal = 2*subtotal

                                #Se va a utilizar el método de Simpson
                                else:
                                    h = (sympify(superior) - sympify(inferior))/(3*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        if count % 2 == 0:
                                            subtotal = subtotal + (2 * sympify(resu[indice]))
                                        else:
                                            subtotal = subtotal + (4 * sympify(resu[indice]))
                                        count += 1

                                integral = h*(float(resu['fx0'])+float(resu[indice_n])+subtotal)
                                texto = " integral ≈ %1.5f " % integral
                                messages.add_message(request, messages.INFO, texto)
                            else:
                                messages.add_message(request, messages.INFO, 'Se necesitan mas valores para aplicar el método')
                        #integral definida simple
                        else:
                            integralDef = integrate(expr,(variable1, inferior1, superior1),(variable, inferior, superior))
                            #integrate(f, (y, 1, 3), (x, 0, 2))
                            texto = " Integral Definida = %1.5f " % integralDef
                            messages.add_message(request, messages.INFO, texto)
                    #Integral indefinida
                    else:
                        integralInd = integrate(expr,variable)
                        texto = " Integral Indefinida = "+str(integralInd)
                        messages.add_message(request, messages.INFO, texto)
                #else:
                    #messages.add_message(request, messages.SUCCESS, 'Función: '+str_expr)
            except (TypeError, AttributeError, SympifyError):
                messages.add_message(request, messages.INFO, 'Expresión inválida')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FuncionDobleForm()
    return render(request, 'integralesDobles.html', {'form': form})


def menu(request):
    return render(request, "menu.html", {})

def graficarFuncion_ajax(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        inferior = request.POST['inferior']
        superior = request.POST['superior']
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        #gr = grafico.graficar_funcion(expr, funcion, inferior, superior, estilo)
        gr = grafico.graficar_funcion(expr, funcion, inferior, superior, estilo)
        #y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': gr })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('integrales.html', context_instance=RequestContext(request))

def graficarFuncion3d_ajax(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        inferior = request.POST['inferior']
        superior = request.POST['superior']
        inferior1 = request.POST['inferior1']
        superior1 = request.POST['superior1']
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        #gr = grafico.graficar_funcion(expr, funcion, inferior, superior, estilo)
        gr = grafico.graficar_funcion1(expr, funcion, inferior, superior, inferior1, superior1, estilo)
        #y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': gr })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('integralesDobles.html', context_instance=RequestContext(request))

def biseccion(request):
    form = BiseccionForm()
    return render(request, 'biseccion.html', {'form': form})

def graficarBiseccion_ajax(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        inferior = request.POST['inferior']
        superior = request.POST['superior']
        limpiar = request.POST['limpiar']
        #error = 0.05
        error = request.POST['error']
        if (int(limpiar) == 1):
            for f in glob.glob("Tesis/static/imagenes/foo*.jpeg"):
                os.remove(f)
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        gr = grafico.graficar_biseccion(expr, funcion, inferior, superior, estilo, error)
        if (gr['error'] == 0):
            response_dict = {}
            response_dict.update({'server_response': gr })
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        else:
            return HttpResponse("Para aplicar el método se debe verificar el teorema de Bolzano (f(a)*f(b)<0)", status=404)
    else:
        return render_to_response('biseccion.html', context_instance=RequestContext(request))

def derivadas(request):
    form = DerivadaForm()
    return render(request, 'derivadas.html', {'form': form})

def graficarDerivada_ajax(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        inf = request.POST['inf']
        sup = request.POST['sup']
        limpiar = request.POST['limpiar']
        if (int(limpiar) == 1):
            for f in glob.glob("Tesis/static/imagenes/foo*.jpeg"):
                os.remove(f)
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        expr = sympify(funcion)
        derivada = diff (expr, variable)
        #gr = grafico.graficar_biseccion(expr, funcion, inferior, superior, estilo, error)
        gr = grafico.graficar_derivada(expr, funcion, inf, sup, estilo, derivada, variable)
        #y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': gr })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('integrales.html', context_instance=RequestContext(request))
