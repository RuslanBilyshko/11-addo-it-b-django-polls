from django import forms


class FieldHandler:
    formfields = {}
    attrs = {'class': 'nocopy', }

    def __init__(self, fields):
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_" + field['type'])(field, options)
            self.formfields[field['name']] = f

    def get_options(self, field):
        options = {}
        options['label'] = field.get("label", None)
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0))
        options['initial'] = field.get("value", '')
        return options

    def create_field_for_hidden(self, field, options):
        return forms.CharField(widget=forms.HiddenInput(attrs={'value': field.get("value", '')}), **options)

    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "20"))
        return forms.CharField(**options)

    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999"))
        return forms.CharField(widget=forms.Textarea, **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999"))
        options['min_value'] = int(field.get("min_value", "-999999999"))
        return forms.IntegerField(**options)

    def create_field_for_radio(self, field, options):
        options['choices'] = [(c['value'], c['name']) for c in field['choices']]
        return forms.ChoiceField(widget=forms.RadioSelect(attrs=self.attrs), **options)

    def create_field_for_select(self, field, options):
        options['choices'] = [(c['value'], c['name']) for c in field['choices']]
        return forms.ChoiceField(**options)

    def create_field_for_multiple_select(self, field, options):
        options['choices'] = [(c['value'], c['name']) for c in field['choices']]
        options['widget'] = forms.SelectMultiple()
        return forms.MultipleChoiceField(**options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)

    def create_field_for_multiple_checkbox(self, field, options):
        options['choices'] = [(c['value'], c['name']) for c in field['choices']]
        options['widget'] = forms.CheckboxSelectMultiple()
        return forms.MultipleChoiceField(**options)


def get_form(jstr):
    fh = FieldHandler(jstr)
    return type('DynaForm', (forms.Form,), fh.formfields)






