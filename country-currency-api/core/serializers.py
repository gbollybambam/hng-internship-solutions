from rest_framework import serializers
from .models import Country, Status

class CountrySerializer(serializers.ModelSerializer):
    last_refreshed_at = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'capital',
            'region',
            'population',
            'currency_code',
            'exchange_rate',
            'estimated_gdp',
            'flag_url',
            'last_refreshed_at',
        ]

    def get_last_refreshed_at(self, obj):
        if not hasattr(self, '_last_refreshed_at'):
            try:
                status = Status.objects.latest('pk')
                self._last_refreshed_at = status.last_refreshed_at
            except Status.DoesNotExist:
                self._last_refreshed_at = None
            
        return self._last_refreshed_at
