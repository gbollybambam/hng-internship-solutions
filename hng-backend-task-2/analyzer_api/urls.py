from django.urls import path
from .views import StringListCreateView, StringDetailDeleteView, NaturalLanguageFilterView

urlpatterns = [
    path('', StringListCreateView.as_view(), name='string-list-create'),
    path('filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='natural-language-filter'),
    path('<path:string_value>/', StringDetailDeleteView.as_view(), name='string-detail-delete'),
]
