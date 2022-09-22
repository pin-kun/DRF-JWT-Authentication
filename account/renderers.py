from rest_framework import renderers
import json

# bu default we are getting 'serializers.error' in 'views.py' file but It will just mention the field name which have errors in it.
# Here we are creating a custom error message which will shows all type of error (related to serializer) under the name of "error"
# Mostly will be helpful in fornt-end. It will indicate that "these are the field which have error"
class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'error': data})
        else:
            response = json.dumps(data)
        
        return response
        