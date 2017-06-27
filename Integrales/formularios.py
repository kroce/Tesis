from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import join, default
from django.utils.safestring import mark_safe
import json
from FieldHandler import FieldHandler

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class FuncionForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':16}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Limite Inferior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Limite Superior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    definida = forms.BooleanField(label='Integracion Definida', initial=False, required=False)
    numerica = forms.BooleanField(label='Integracion Numerica', initial=False, required=False)
    RADIO_CHOICES = (
        ('trapecio', "Trapecio"),
        ('simpson', "Simpson"),
    )
    formula = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=RADIO_CHOICES, required=False)
    x0 = forms.CharField(label='x0', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx0 = forms.CharField(label='fx0', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    x1 = forms.CharField(label='x1', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx1 = forms.CharField(label='fx1', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    x2 = forms.CharField(label='x2', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx2 = forms.CharField(label='fx2', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    x3 = forms.CharField(label='x3', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx3 = forms.CharField(label='fx3', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    x4 = forms.CharField(label='x4', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx4 = forms.CharField(label='fx4', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    x5 = forms.CharField(label='x5', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    fx5 = forms.CharField(label='fx5', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))

class FuncionDobleForm(forms.Form):
    TIPOINTEGRAL_CHOICES = (
        ('indefinida', "Integral Indefinida"),
        ('definida', "Integral Definida"),
    )
    tipoIntegral = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer, attrs={'style':'width:30px'}),choices=TIPOINTEGRAL_CHOICES, required=False)
    funcion = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Var. 1', required=False, max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    variable1 = forms.CharField(label='Var. 2', required=False, max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    variableInd = forms.CharField(label='Var. 1', required=False, max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    variable1Ind = forms.CharField(label='Var. 2', required=False, max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Lim Inf 1', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Lim Sup 1', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior1 = forms.CharField(label='Lim Inf 2', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior1 = forms.CharField(label='Lim Sup 2', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    # definida = forms.BooleanField(label='Integracion Definida', initial=False, required=False)
    # numerica = forms.BooleanField(label='Integracion Numerica', initial=False, required=False)
    # RADIO_CHOICES = (
    #     ('trapecio', "Trapecio"),
    #     ('simpson', "Simpson"),
    # )
    # formula = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=RADIO_CHOICES, required=False)
    # x0 = forms.CharField(label='x0', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx0 = forms.CharField(label='fx0', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # x1 = forms.CharField(label='x1', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx1 = forms.CharField(label='fx1', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # x2 = forms.CharField(label='x2', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx2 = forms.CharField(label='fx2', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # x3 = forms.CharField(label='x3', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx3 = forms.CharField(label='fx3', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # x4 = forms.CharField(label='x4', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx4 = forms.CharField(label='fx4', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # x5 = forms.CharField(label='x5', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))
    # fx5 = forms.CharField(label='fx5', required=False, widget=forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}))

class BiseccionForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Cota Inferior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Cota Superior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    error = forms.CharField(label='Error', required=False, widget=forms.TextInput(attrs={'size' : '5'}))

class NewtonForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    x0 = forms.CharField(label='x0', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    error = forms.CharField(label='Error', required=False, widget=forms.TextInput(attrs={'size' : '5'}))

class DerivadaForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inf = forms.CharField(label='inf', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    sup = forms.CharField(label='sup', required=False, widget=forms.TextInput(attrs={'size' : '5'}))

class Integralesform(forms.Form):
    def get_form(self):
        jstr = open('Tesis/fields_integrales.json')
        fields=json.load(jstr)
        fh = FieldHandler(fields)
        return type('Integralesform', (forms.Form,), fh.formfields )

class DerivadaNumform(forms.Form):
    def get_form(self):
        jstr = open('Tesis/fields_derivadaNum.json')
        fields=json.load(jstr)
        fh = FieldHandler(fields)
        return type('DerivadaNumform', (forms.Form,), fh.formfields )

class GraficoFuncionesForm(forms.Form):
     def get_form(self):
        jstr = open('Tesis/fields_multiplesFunc.json')
        fields=json.load(jstr)
        fh = FieldHandler(fields)
        return type('GraficoFuncionesForm', (forms.Form,), fh.formfields )