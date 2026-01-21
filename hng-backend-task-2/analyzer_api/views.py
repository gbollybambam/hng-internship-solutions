from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
# Create your views here.

from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer, StringValueSerializer
from .utils import calculate_sha256, get_character_properties, is_string_palindrome, parse_natural_language_query
from .query_builder import apply_filters_to_queryset

class StringListCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StringValueSerializer(data=request.data)
        if not serializer.is_valid():
            if 'value' not in request.data:
                return Response({ 'error': 'Missing "value" field.' }, status=status.HTTP_400_BAD_REQUEST)
            if 'value' in request.data and not isinstance(request.data['value'], str):
                return Response({'error': 'Invalid data type for "value" (must be string).'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        string_value = serializer.validated_data['value']
        hash_id = calculate_sha256(string_value)

        if AnalyzedString.objects.filter(pk=hash_id).exists():
            return Response({'error': 'String already exists in the system.'}, status=status.HTTP_409_CONFLICT)
        
        properties = get_character_properties(string_value)

        analyzed_string = AnalyzedString(
            id=hash_id,
            value=string_value,
            length=properties['length'],
            is_palindrome=properties['is_palindrome'],
            unique_characters=properties['unique_characters'],
            word_count=properties['word_count'],
            character_frequency_map=properties['character_frequency_map']
        )
        analyzed_string.save()

        response_serializer = AnalyzedStringSerializer(analyzed_string)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        valid_filters = {}
        query_params = request.query_params

        validation_map = {
            'is_palindrome': bool,
            'min_length': int,
            'max_length': int,
            'word_count': int,
            'contains_character': str,
        }

        for key, expected_type in validation_map.items():
            value = query_params.get(key)
            if value is None:
                continue
                
            try:
                if expected_type is bool:
                    if value.lower() not in ['true', 'false']:
                        raise ValueError("Invalid boolean value.")
                    valid_filters[key] = value
                elif expected_type is int:
                    valid_filters[key] = int(value)
                elif expected_type is str and len(value) == 1:
                    valid_filters[key] = value
                elif expected_type is str: 
                    return Response({
                        'error': f'Invalid value for "{key}": must be a single character.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except ValueError:
                return Response({
                    'error': f'Invalid type or value for query parameter "{key}". Expected {expected_type.__name__}.'
                }, status=status.HTTP_400_BAD_REQUEST)

        queryset = AnalyzedString.objects.all()
        filtered_queryset = apply_filters_to_queryset(queryset, query_params.dict()) 

        count = filtered_queryset.count()
        serializer = AnalyzedStringSerializer(filtered_queryset, many=True)
        
        filters_applied = {k: v for k, v in query_params.items() if k in validation_map}

        return Response({
            "data": serializer.data,
            "count": count,
            "filters_applied": filters_applied
        }, status=status.HTTP_200_OK)


class StringDetailDeleteView(APIView):
    def get_object_by_value(self, string_value):
        hash_id = calculate_sha256(string_value)
        try:
            return AnalyzedString.objects.get(pk=hash_id)
        except AnalyzedString.DoesNotExist:
            raise Http404
        
    def get(self, request, string_value, *args, **kwargs):
        try:
            string_obj = self.get_object_by_value(string_value)
            serializer = AnalyzedStringSerializer(string_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'String does not exist in the system.'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, string_value, *args, **kwargs):
        try:
            string_obj = self.get_object_by_value(string_value)
            string_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'error': 'String does not exist in the system.'}, status=status.HTTP_404_NOT_FOUND)
        

class NaturalLanguageFilterView(APIView) :
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'Missing "query" parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed_filters = parse_natural_language_query(query)
            
            queryset = AnalyzedString.objects.all()
            string_filters = {k: str(v) for k, v in parsed_filters.items()}
            filtered_queryset = apply_filters_to_queryset(queryset, string_filters)

            count = filtered_queryset.count()
            serializer = AnalyzedStringSerializer(filtered_queryset, many=True)

            return Response({
                "data": serializer.data,
                "count": count,
                "interpreted_query": {
                    "original": query,
                    "parsed_filters": parsed_filters
                }
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception:
            return Response({'error': 'Unable to parse natural language query.'}, status=status.HTTP_400_BAD_REQUEST)