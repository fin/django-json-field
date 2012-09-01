from django.forms import fields, util
from django.utils import simplejson as json

import datetime

class JSONFormField(fields.Field):

    def __init__(self, *args, **kwargs):
        self.simple = kwargs.pop('simple', False)
        self.encoder_kwargs = kwargs.pop('encoder_kwargs', {})
        self.decoder_kwargs = kwargs.pop('decoder_kwargs', {})
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        # Have to jump through a few hoops to make this reliable
        value = super(JSONFormField, self).clean(value)
        if not isinstance(value, basestring):
            return value

        # allow an empty value on an optional field
        if value is None:
            return value

        ## Got to get rid of newlines for validation to work
        # Data newlines are escaped so this is safe
        try:
            value = json.loads(value)
        except ValueError, e:
            raise util.ValidationError('%s (Caught "%s")' % (self.help_text, e))

        return value

    def bound_data(self, data, initial):
        if isinstance(data, basestring):
            return data
        return json.dumps(data)
