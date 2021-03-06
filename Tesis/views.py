# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Integrales.formularios import FuncionForm
from Integrales.formularios import FuncionDobleForm
from Integrales.formularios import BiseccionForm
from Integrales.formularios import NewtonForm
from Integrales.formularios import DerivadaForm
from Integrales.formularios import DerivadaNumform
from Integrales.formularios import GraficoFuncionesForm

from sympy import *
from django.contrib import messages
from Tesis.Graficos import Grafico
from Tesis.Metodos import Metodos
import os
import glob
import io
import json
import socket
from Integrales.formularios import Integralesform

# Create your views here.


def definirCamposIntegrales():
    fields = []
    cantidad = 10
    fields.append({"required": 0, "type": "text",
                   "name": "cantidad", "label": "cant", "max_length": 100})

    choices = [{"name": "Integral Definida", "value": "definida"},
               {"name": "Integral Indefinida", "value": "indefinida"},
               {"name": "Integral Numérica", "value": "numerica"}]
    fields.append({"required": 0, "type": "radio",
                   "name": "tipoIntegral", "label": "", "choices": choices})

    fields.append({"required": 0, "type": "text",
                   "name": "funcion", "label": "Función", "max_length": 100})
    fields.append({"required": 0, "type": "text",
                   "name": "variable", "label": "Variable", "max_length": 10})
    fields.append({"required": 0, "type": "text",
                   "name": "inferior", "label": "Limite Inferior"})
    fields.append({"required": 0, "type": "text",
                   "name": "superior", "label": "Limite Superior"})
    fields.append({"required": 0, "type": "text",
                   "name": "indice", "label": " "})
    fields.append({"required": 0, "initial": False, "type": "checkbox",
                   "name": "definida", "label": "Integracion Definida"})
    choices = [{"name": "Trapecio", "value": "trapecio"},
               {"name": "Simpson 1/3", "value": "simpson"}]
    fields.append({"required": 0, "type": "radio",
                   "name": "formula", "label": "", "choices": choices})
    for x in xrange(0, cantidad):
        variable = 'x' + str(x)
        funcion = 'fx' + str(x)
        fields.append({"type": "table", "name": str(variable),
                       "label": str(variable), "required": 0})
        fields.append({"type": "table", "name": str(funcion),
                       "label": str(funcion), "required": 0})

    archivo = open("fields_integrales.json", "w")
    json.dump(fields, archivo, indent=4)
    archivo.close()


def definirCamposDerivadaNumerica():
    fields = []
    cantidad = 10
    
    for x in xrange(0, cantidad):
        variable = 'x' + str(x)
        funcion = 'fx' + str(x)
        fields.append({"type": "table", "name": str(variable),
                       "label": str(variable), "required": 0})
        fields.append({"type": "table", "name": str(funcion),
                       "label": str(funcion), "required": 0})

    archivo = open("fields_derivadaNum.json", "w")
    json.dump(fields, archivo, indent=4)
    archivo.close()

def definirCamposGraficarFciones():
    fields = []
    cantidad = 5
    for x in xrange(1, cantidad):
        funcion = 'funcion' + str(x)
        fields.append({"required": 0, "type": "text",
                "name":str(funcion), "label":str(funcion), "max_length": 100})
       
    fields.append({"required": 0, "type": "text",
                "name": "variable", "label": "Variable", "max_length": 10})
    
    fields.append({"required": 0, "type": "text",
        "name": "inferior", "label": "Limite Inferior"})
    
    fields.append({"required": 0, "type": "text",
                   "name": "superior", "label": "Limite Superior"})
    
    archivo = open("fields_multiplesFunc.json", "w")
    json.dump(fields, archivo, indent=4)
    archivo.close()

def auxiliar(datos):
    i = 0
    x = 'x' + str(i)
    fx = 'fx' + str(i)
    while (x != ""):
        x = 'x' + str(i)
        fx = 'fx' + str(i)
        x, fx = datos[x], datos[fx]
        i = i + 1
    ene = i - 2
    xn = 'x' + str(ene)
    return {'ene': ene, 'x0': datos['x0'], 'xn': datos[xn]}

def grafico1var(request):
    definirCamposGraficarFciones()
    form = GraficoFuncionesForm()
    form_class = form.get_form()
    data = {}

    # Recupera funciones a graficar del post
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            i = 0
            funcion = 'funcion' + str(i)
            while (funcion != ""):
                funcion = 'funcion' + str(i)
                x = form.cleaned_data[funcion]
                i = i + 1
            n = i - 2
            funcionn = 'funcion' + str(ene)
            funcion0 = form.cleaned_data['funcion0']
    else:
        form = form_class()
    return render(request, 'grafico1var.html', {'form': form, 'data': data})

def grafico2var(request):
    form = FuncionDobleForm()
    return render(request, 'grafico2var.html', {'form': form})

def graficarFunciones(request):
    if request.POST.has_key('funcion1'):
        funcion1 = request.POST['funcion1']
        funcion2 = request.POST['funcion2']
        funcion3 = request.POST['funcion3']
        funcion4 = request.POST['funcion4']
        funcion5 = request.POST['funcion5']
        
        variable = request.POST['variable']
        inferior = request.POST['inferior']
        superior = request.POST['superior']
        limpiar = request.POST['limpiar']
        if (int(limpiar) == 1):
            for f in glob.glob("Tesis/static/imagenes/foo*.jpeg"):
                os.remove(f)
        # expr = sympify(funcion1)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()

        funciones = [funcion1, funcion2, funcion3, funcion4, funcion5]
        gr = grafico.funciones(inferior, superior, estilo, variable, funciones)
        response_dict = {}
        response_dict.update({'server_response': gr})
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('grafico1var.html', context_instance=RequestContext(request))

def graficarFuncion3D(request):
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
        gr = grafico.graficar_funcion1(
            expr, funcion, inferior, superior, inferior1, superior1, estilo)
        response_dict = {}
        response_dict.update({'server_response': gr})
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('integralesDobles.html', context_instance=RequestContext(request))

def integrales(request):
    x, y, z = symbols('x y z')
    definirCamposIntegrales()
    form = Integralesform()
    form_class = form.get_form()
    data = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # definida = form.cleaned_data['definida']
            tipoIntegral = form.cleaned_data['tipoIntegral']
            # numerica = form.cleaned_data['numerica']
            
            if 'integrar' in request.POST:
                # Integral Numérica
                if tipoIntegral == 'numerica':
                    resu = auxiliar(form.cleaned_data)
                    n = resu['ene']
                    x0 = resu['x0']
                    xn = resu['xn']
                    if (n >= 1):
                        indice_n = "fx" + str(n)
                        count = 1
                        subtotal = 0
                        # Se va a utilizar el método del trapecio
                        formula = form.cleaned_data['formula']
                        if formula == 'trapecio':
                            h = (sympify(xn) -
                                    sympify(x0)) / (2 * n)
                            while count < n:
                                indice = "fx" + str(count)
                                subtotal = subtotal + \
                                    sympify(form.cleaned_data[indice])
                                count += 1
                            subtotal = 2 * subtotal
                            
                        # Se va a utilizar el método de Simpson
                        else:
                            h = (sympify(xn) -
                                    sympify(x0)) / (3 * n)
                            while count < n:
                                indice = "fx" + str(count)
                                if count % 2 == 0:
                                    subtotal = subtotal + \
                                        (2 *
                                            sympify(form.cleaned_data[indice]))
                                else:
                                    subtotal = subtotal + \
                                        (4 *
                                            sympify(form.cleaned_data[indice]))
                                count += 1

                        integral = h * \
                            (float(form.cleaned_data[
                                'fx0']) + float(form.cleaned_data[indice_n]) + subtotal)
                        texto = " integral ≈ %1.5f " % integral
                        messages.add_message(
                            request, messages.INFO, texto)
                    else:
                        messages.add_message(request, messages.INFO, 'Se necesitan mas valores para aplicar el método')
                # si se va a calcular la integral definida
                else: 
                    try:
                        str_expr = form.cleaned_data['funcion']
                        variable = sympify(form.cleaned_data['variable'])
                        expr = sympify(str_expr)
                        resu = expr.evalf()
                        if tipoIntegral == 'definida':
                            # Integral Definida
                            inferior = form.cleaned_data['inferior']
                            superior = form.cleaned_data['superior']
                            if (inferior!="") & (superior!=""):
                                integralDef = integrate(expr, (variable, inferior, superior))
                                texto = " Integral Definida = %1.5f " % integralDef
                                messages.add_message(request, messages.INFO, texto)
                            else:
                                messages.add_message(request, messages.INFO, 'Se requieren los valores del intervalo')
                        # Integral indefinida
                        else:
                            integralInd = integrate(expr, variable)
                            texto = " Integral Indefinida = " + str(integralInd)
                            messages.add_message(request, messages.INFO, texto)
                    except (TypeError, AttributeError, SympifyError):
                        messages.add_message(request, messages.INFO, 'Expresión inválida')
        else:
            print 'formulario inválido'

    # if a GET (or any other method) we'll create a blank form
    else:
        form = form_class()
        # form = FuncionForm()

    return render(request, 'integrales.html', {'form': form, 'data': data})


def integralesDobles(request):

    x, y, z = symbols('x y z')
    if request.method == 'POST':
        form = FuncionDobleForm(request.POST)
        if form.is_valid():
            tipoIntegral = form.cleaned_data['tipoIntegral']
            str_expr = form.cleaned_data['funcion']
            try:
                expr = sympify(str_expr)
                resu = expr.evalf()
                if 'integrar' in request.POST:

                    # Integral Definida
                    if tipoIntegral == 'definida':
                        variable = sympify(form.cleaned_data['variable'])
                        variable1 = sympify(form.cleaned_data['variable1'])
                        inferior = form.cleaned_data['inferior']
                        superior = form.cleaned_data['superior']
                        inferior1 = form.cleaned_data['inferior1']
                        superior1 = form.cleaned_data['superior1']
                        integralDef = integrate(
                            expr, (variable1, inferior1, superior1), (variable, inferior, superior))
                        texto = " Integral Definida = %1.5f " % integralDef
                        messages.add_message(request, messages.INFO, texto)

                    # Integral indefinida
                    if tipoIntegral == 'indefinida':
                        variable = sympify(form.cleaned_data['variableInd'])
                        texto = " Integral Indefinida = " + str(integrate(expr, variable))
                        messages.add_message(request, messages.INFO, texto)
                    
                    # Integral numerica
                    if tipoIntegral == 'numerica':
                        variable = sympify(form.cleaned_data['variableInd'])
                        variable1 = sympify(form.cleaned_data['variable1Ind'])
                        a = float(form.cleaned_data['a'])
                        b = float(form.cleaned_data['b'])
                        c = float(form.cleaned_data['c'])
                        d = float(form.cleaned_data['d'])
                        m = int(form.cleaned_data['m'])
                        n = int(form.cleaned_data['n'])
                        metodo = Metodos()
                        formula = form.cleaned_data['formula']
                        if formula == 'trapecio':
                            resultado = metodo.trapecio2D(expr, variable, variable1, a, b, c, d, m, n)
                        if formula == 'simpson':
                            resultado = metodo.simpson2D(expr, variable, variable1, a, b, c, d, m, n)
                        
                        texto = " integral ≈ %1.5f " % resultado['aproximacion']
                        messages.add_message(request, messages.INFO, texto)
            except (TypeError, AttributeError, SympifyError):
                messages.add_message(
                    request, messages.INFO, 'Expresión inválida')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FuncionDobleForm()
    return render(request, 'integralesDobles.html', {'form': form})


def menu(request):
    return render(request, "menu.html", {})

def ayuda(request):
    return render(request, "ayuda.html", {})

def graficarFuncion(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        inferior = request.POST['inferior']
        superior = request.POST['superior']
        sombra = request.POST['sombra']
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        gr = grafico.graficarFuncion(expr, funcion, variable, inferior, superior, estilo, sombra)
        response_dict = {}
        response_dict.update({'server_response': gr})
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('integrales.html', context_instance=RequestContext(request))

def graficarBiseccion_ajax(request):
    if request.POST.has_key('funcion'):
        try:
            funcion = request.POST['funcion']
            if (funcion == ''):
                return HttpResponse('Debe ingresar la función') 
            expr = sympify(funcion)
            variable = request.POST['variable']
            if (variable == ''):
                return HttpResponse('Debe ingresar la variable') 
            inferior = request.POST['inferior']
            if (inferior == ''):
                return HttpResponse('Debe ingresar la cota inferior') 
            superior = request.POST['superior']
            if (superior == ''):
                return HttpResponse('Debe ingresar la cota superior') 
            error = request.POST['error']
            if (error == ''):
                return HttpResponse('Debe ingresar el error') 
            limpiar = request.POST['limpiar']
            if (int(limpiar) == 1):
                for f in glob.glob("Tesis/static/imagenes/foo*.jpeg"):
                    os.remove(f)
            grafico = Grafico()
            estilo = grafico.estilo1()
            grafico.agregarEjes()
            gr = grafico.graficar_biseccion(
                expr, funcion, inferior, superior, estilo, error)
            if (gr['error'] == 0):
                response_dict = {}
                response_dict.update({'server_response': gr})
                return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
            else:
                return HttpResponse("Para aplicar el método se debe verificar el teorema de Bolzano (f(a)*f(b)<0)", status=404)
        except (TypeError, AttributeError, SympifyError):
            return HttpResponse('Expresión inválida') 
    else:
        form = BiseccionForm()
        return render(request, 'biseccion.html', {'form': form})
        
def graficarNewton_ajax(request):
    if request.POST.has_key('funcion'):
        funcion = request.POST['funcion']
        variable = request.POST['variable']
        x0 = request.POST['x0']
        limpiar = request.POST['limpiar']
        error = request.POST['error']
        expr = sympify(funcion)
        derivada = diff(expr, variable)
        if (int(limpiar) == 1):
            for f in glob.glob("Tesis/static/imagenes/foo*.jpeg"):
                os.remove(f)
        expr = sympify(funcion)
        grafico = Grafico()
        estilo = grafico.estilo1()
        grafico.agregarEjes()
        gr = grafico.graficar_newton(
            expr, funcion, x0, derivada, estilo, error)
        if (gr['error'] == 0):
            response_dict = {}
            response_dict.update({'server_response': gr})
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        else:
            return HttpResponse("Para aplicar el método se debe verificar el teorema de Bolzano (f(a)*f(b)<0)", status=404)
    else:
        form = NewtonForm()
        return render(request, 'newton.html', {'form': form})

def derivadas(request):
    form = DerivadaForm()
    return render(request, 'derivadas.html', {'form': form})

def derivadaNumerica(request):
    definirCamposDerivadaNumerica()
    form = DerivadaNumform()
    form_class = form.get_form()
    data = {}
    derivadaNumerica = 0
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            resu = auxiliar(form.cleaned_data)
            n = resu['ene']
            if (n >= 1):
                indice_n = "fx" + str(n)
                count = 0
                subtotal = 0

            flag = 1
            h = 0
            fpunto = 0
            fadelante = 0
            fatras = 0
            while count <= n and (flag):
                indice = "x" + str(count)
                indicef = "fx" + str(count)
                dato = form.cleaned_data[indice]  # xi
                fdato = form.cleaned_data[indicef]  # f(xi)
                punto = form.cleaned_data['punto']  # x0
                tipo = form.cleaned_data['tipo']

                # Si es derivada hacia adelante, busco el primer punto mayor a
                # x0
                if tipo == "adelante":
                    if sympify(dato) == sympify(punto):
                        fpunto = fdato
                    if sympify(dato) > sympify(punto):
                        h = sympify(dato) - sympify(punto)
                        derivadaNumerica = (
                            sympify(fdato) - sympify(fpunto)) / sympify(h)
                        flag = 0

                if tipo == "atras":
                    if sympify(dato) < sympify(punto):
                        h = sympify(punto) - sympify(dato)
                        fpunto = fdato
                    if sympify(dato) == sympify(punto):
                        derivadaNumerica = (
                            sympify(fdato) - sympify(fpunto)) / sympify(h)

                if tipo == "central":
                    if sympify(dato) < sympify(punto):
                        h = sympify(punto) - sympify(dato)
                        fatras = fdato
                    if sympify(dato) > sympify(punto):
                        if round((sympify(dato) - sympify(punto)), 1) == round(sympify(h), 1):
                            fadelante = fdato
                    if fatras != 0 and fadelante != 0:
                        print "fatras " + str(fatras)
                        print "fadelante " + str(fadelante)
                        print "h " + str(h)
                        derivadaNumerica = (
                            sympify(fadelante) - sympify(fatras)) / (2 * sympify(h))

                count += 1

            texto = " Derivada Numérica ≈ %1.5f " % derivadaNumerica
            messages.add_message(request, messages.INFO, texto)
    else:
        form = form_class()
    return render(request, 'derivadaNumerica.html', {'form': form, 'data': data})

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
        # expr = sympify(funcion)
        derivada = diff(expr, variable)
        variables = ['x','y','z'];
        band = false;
        for x in xrange(0, len(variables)):
            if (str(variable)!=variables[x] and variables[x] in str(expr) ):
                band = true;
                break;
        # si hay una constante no puedo graficar
        if band:
            gr = {'filename':'', 'funcion':str(expr), 'derivada': str(derivada)}
            response_dict = {}
            response_dict.update({'server_response': gr})
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        else:
            gr = grafico.graficar_derivada(expr, funcion, inf, sup, estilo, derivada, variable)
            response_dict = {}
            response_dict.update({'server_response': gr})
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('derivadas.html', context_instance=RequestContext(request))

def derivadaAjax(request):
    if request.POST.has_key('funcion'):

        funcion = request.POST['funcion']
        tipo = request.POST['tipo']
        punto = request.POST['punto']
        derivada = {'derivada': 'dsadsad'}
        response_dict = {}

        response_dict.update({'server_response': derivada})
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        return render_to_response('derivadaNumerica.html', context_instance=RequestContext(request))
