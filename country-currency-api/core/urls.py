from django.urls import path
from .views import RefreshCountriesView, CountryListView, CountryDetailView, CountryDestroyView, StatusView, SummaryImageView

urlpatterns = [
    path('countries/refresh', RefreshCountriesView.as_view(), name='refresh-countries'),
    path('countries', CountryListView.as_view(), name='country-list'),
    path('countries/image', SummaryImageView.as_view(), name='summary-image'),
    path('countries/<str:name>', CountryDetailView.as_view(), name='country-detail'),
    path('countries/<str:name>/delete', CountryDestroyView.as_view(), name='country-destroy'),
    path('status', StatusView.as_view(), name='status'),
]
