from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            raw_details = response.data
            
            if isinstance(raw_details, dict):
                formatted_details = {}
                for field, errors in raw_details.items():
                    if isinstance(errors, list) and errors:
                        formatted_details[field] = errors[0]
                    else:
                        formatted_details[field] = errors
                
                response.data = {
                    'error': 'Validation failed',
                    'details': formatted_details
                }
            else:
                response.data = {
                    'error': 'Validation failed'
                }
        
        elif response.status_code == 404:
            response.data = {'error': 'Country not found'}
        
        elif response.status_code == 500:
            response.data = {'error': 'Internal server error'}
        
        elif response.status_code == 405:
            response.data = {'error': f'Method "{context["request"].method}" not allowed.'}

    return response