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
import os, glob, io
import json
import socket
from Integrales.formularios import Integralesform

# Create your views here.

def definirCamposIntegrales():
    fields = [];
    cantidad = 10
    fields.append({"required": 0, "type": "text", "name": "cantidad","label": "cant", "max_length": 100})
    fields.append({"required": 1, "type": "text", "name": "funcion","label": "Función", "max_length": 100})
    fields.append({"required": 1, "type": "text", "name": "variable","label": "Variable", "max_length": 10})
    fields.append({"required": 0, "type": "text", "name": "inferior","label": "Limite Inferior"})
    fields.append({"required": 0, "type": "text", "name": "superior","label": "Limite Superior"})
    fields.append({"required": 0, "type": "text", "name": "indice","label": " "})
    fields.append({"required": 0, "initial":False, "type": "checkbox", "name": "definida","label": "Integracion Definida"})
    fields.append({"required": 0, "initial":False, "type": "checkbox", "name": "numerica","label": "Integracion Numerica"})
    choices = [{"name": "Trapecio","value": "trapecio"}, {"name": "Simpson","value": "simpson"}]
    fields.append({"required": 0, "type": "radio", "name": "formula","label": "", "choices": choices})
    for x in xrange(0, cantidad):
        variable =  'x'+str(x)
        funcion =  'fx'+str(x)
        fields.append({"type": "table", "name": str(variable), "label": str(variable), "required":0})
        fields.append({"type": "table", "name": str(funcion), "label": str(funcion), "required":0})

    archivo = open("fields_integrales.json","w")
    json.dump(fields,archivo, indent=4)
    archivo.close()

def auxiliar(datos):
    i = 0
    x = 'x'+str(i);
    fx = 'fx'+str(i)
    while (x != ""):
        x = 'x'+str(i)
        fx = 'fx'+str(i)
        #x0, fx0 = datos['x0'], datos['fx0']
        x, fx = datos[x], datos[fx]
        i=i+1
    ene = i-2
    return {'ene':ene}

#algo similar para integrales dobles, un método similar a éste
def integrales(request):
    #ver como hago para obtener todos los simbolos de la funcion para declararlos
    x, y, z = symbols('x y z')
    #Agrego
    definirCamposIntegrales()
    form = Integralesform()
    form_class = form.get_form()
    data = {}
    #hasta aca, comento la sig
    if request.method == 'POST':
        form = form_class(request.POST)
        #form = FuncionForm(request.POST)
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
                                print "aca "+indice_n
                                count = 1
                                subtotal = 0
                                #Se va a utilizar el método del trapecio
                                if formula == 'trapecio':
                                    h = (sympify(superior) - sympify(inferior))/(2*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        subtotal = subtotal + sympify(form.cleaned_data[indice])
                                        count += 1
                                    subtotal = 2*subtotal

                                #Se va a utilizar el método de Simpson
                                else:
                                    h = (sympify(superior) - sympify(inferior))/(3*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        if count % 2 == 0:
                                            subtotal = subtotal + (2 * sympify(form.cleaned_data[indice]))
                                        else:
                                            subtotal = subtotal + (4 * sympify(form.cleaned_data[indice]))
                                        count += 1
                                print form.cleaned_data['fx0']
                                print
                                print form.cleaned_data[indice_n]
                                integral = h*(float(form.cleaned_data['fx0'])+float(form.cleaned_data[indice_n])+subtotal)
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
        form = form_class()
        #form = FuncionForm()

    return render(request, 'integrales.html', {'form': form, 'data' : data})

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
                                        subtotal = subtotal + sympify(form.cleaned_data[indice])
                                        count += 1
                                    subtotal = 2*subtotal

                                #Se va a utilizar el método de Simpson
                                else:
                                    h = (sympify(superior) - sympify(inferior))/(3*n)
                                    while count < n:
                                        indice = "fx"+str(count)
                                        if count % 2 == 0:
                                            subtotal = subtotal + (2 * sympify(form.cleaned_data[indice]))
                                        else:
                                            subtotal = subtotal + (4 * sympify(form.cleaned_data[indice]))
                                        count += 1

                                integral = h*(float(form.cleaned_data['fx0'])+float(form.cleaned_data[indice_n])+subtotal)
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
