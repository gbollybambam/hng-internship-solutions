from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .services import refresh_country_data, ExternalAPIError
from .serializers import CountrySerializer
from .models import Country, Status
from django.shortcuts import get_object_or_404
import os
from django.http import FileResponse
from django.conf import settings
# Create your views here.

class RefreshCountriesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_country_data()
            return Response(
                {"message": "Country data refreshed successfully."},
                status=status.HTTP_200_OK
            )
        except ExternalAPIError as e:
            api_name = str(e)
            return Response(
                {"error": "External data source unavailable", "details": f"Could not fetch data from {api_name}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CountryListView(generics.ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all()
        region = self.request.query_params.get('region')
        currency = self.request.query_params.get('currency')
        sort_by = self.request.query_params.get('sort')

        if region:
            queryset = queryset.filter(region__iexact=region)

        if currency:
            queryset = queryset.filter(currency_code__iexact=currency)

        if sort_by == 'gdp_desc':
            queryset = queryset.order_by('-estimated_gdp')
    
        return queryset

class StatusView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            status_obj = Status.objects.latest('pk')
            response_data = {
                "total_countries": status_obj.total_countries,
                "last_refreshed_at": status_obj.last_refreshed_at
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Status.DoesNotExist:
            return Response({
                "total_countries": 0,
                "latest_refreshed_at": None
            }, status=status.HTTP_200_OK)

class CountryDetailView(generics.RetrieveAPIView):
    serializer_class = CountrySerializer

    def get_object(self):
        name = self.kwargs['name']
        queryset = Country.objects.all()
        obj = get_object_or_404(queryset, name__iexact=name)
        return obj

class CountryDestroyView(generics.DestroyAPIView):
    queryset = Country.objects.all()
    lookup_field = 'name'

    def get_object(self):
        name = self.kwargs[self.lookup_field]
        obj = get_object_or_404(Country, name__iexact=name)
        return obj
    
class SummaryImageView(APIView):
    def get(self, request, *args, **kwargs):
        image_path = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')

        if os.path.exists(image_path):
            return FileResponse(open(image_path, 'rb'), content_type='image/png')
        else:
            return Response(
                {"error": "Summary image not found"},
                status=status.HTTP_404_NOT_FOUND
            )