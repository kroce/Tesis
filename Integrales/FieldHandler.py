import django.forms
from django.utils.safestring import mark_safe

class HorizRadioRenderer(django.forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class FieldHandler():

    formfields = {}
    def __init__(self, fields):
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_"+field['type'] )(field, options)
            self.formfields[field['name']] = f

    def get_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )
        return options

    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "20") )
        return django.forms.CharField(widget=django.forms.TextInput(attrs={'size' : 16}),**options)

    def create_field_for_table(self, field, options):
        options['max_length'] = int(field.get("max_length", "20") )
        return django.forms.CharField(widget=django.forms.TextInput(attrs={'style' : 'border:1px solid transparent;'}),**options)

    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999") )
        return django.forms.CharField(widget=django.forms.Textarea, **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999") )
        options['min_value'] = int(field.get("min_value", "-999999999") )
        return django.forms.IntegerField(**options)

    def create_field_for_float(self, field, options):
        options['max_value'] = float(field.get("max_value", "999999999") )
        options['min_value'] = float(field.get("min_value", "-999999999") )
        return django.forms.FloatField(**options)

    def create_field_for_radio(self, field, options):
        options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return django.forms.ChoiceField(widget=django.forms.RadioSelect(renderer=HorizRadioRenderer, attrs={'style':'width:30px'}),   **options)
        #widget=forms.RadioSelect(renderer=HorizRadioRenderer)

    def create_field_for_select(self, field, options):
        options['choices']  = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return django.forms.ChoiceField(  **options)

    def create_field_for_checkbox(self, field, options):
        options['initial'] = bool(field.get("initial", False) )
        return django.forms.BooleanField(widget=django.forms.CheckboxInput, **options)
