from json_field.forms import JSONFormField

from django.forms import Form

class TestForm(Form):
    json = JSONFormField()

class OptionalForm(Form):
    json = JSONFormField(required=False)
