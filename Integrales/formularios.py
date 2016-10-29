from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import join, default
from django.utils.safestring import mark_safe


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class FuncionForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Limite Inferior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Limite Superior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    definida = forms.BooleanField(label='Integracion Definida', initial=False, required=False)
    numerica = forms.BooleanField(label='Integracion Numerica', initial=False, required=False)
    RADIO_CHOICES = (
        ('trapecio', "Trapecio"),
        ('simpson', "Simpson"),
    )
    # although I've abbreviated the model, 'rad' does not appear in the model;
    # it merely provides input to the un-provided clean function
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
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable 1', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    variable1 = forms.CharField(label='Variable 2', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Limite Inferior 1', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Limite Superior 1', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior1 = forms.CharField(label='Limite Inferior 2', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior1 = forms.CharField(label='Limite Superior 2', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    definida = forms.BooleanField(label='Integracion Definida', initial=False, required=False)
    numerica = forms.BooleanField(label='Integracion Numerica', initial=False, required=False)
    RADIO_CHOICES = (
        ('trapecio', "Trapecio"),
        ('simpson', "Simpson"),
    )
    # although I've abbreviated the model, 'rad' does not appear in the model;
    # it merely provides input to the un-provided clean function
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

class BiseccionForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inferior = forms.CharField(label='Cota Inferior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    superior = forms.CharField(label='Cota Superior', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    error = forms.CharField(label='Error', required=False, widget=forms.TextInput(attrs={'size' : '5'}))

class DerivadaForm(forms.Form):
    funcion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size' : '16'}))
    variable = forms.CharField(label='Variable', max_length=10, widget=forms.TextInput(attrs={'size' : '5'}))
    inf = forms.CharField(label='inf', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
    sup = forms.CharField(label='sup', required=False, widget=forms.TextInput(attrs={'size' : '5'}))
