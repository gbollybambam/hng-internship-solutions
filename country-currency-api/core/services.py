import requests
import random
from datetime import datetime, timezone

from .models import Country, Status
from .image_generator import generate_summary_image

COUNTRIES_API_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_RATE_API_URL = "https://open.er-api.com/v6/latest/USD"

class ExternalAPIError(Exception):
    pass

def refresh_country_data():
    try:
        print("Fetching exchhange rates")
        exchange_response = requests.get(EXCHANGE_RATE_API_URL, timeout=10)
        exchange_response.raise_for_status()
        rates = exchange_response.json().get('rates', {})
    except requests.exceptions.RequestException:
        raise ExternalAPIError("open.er-api.com")

    try:
        print("Fetching country data...")
        countries_response = requests.get(COUNTRIES_API_URL, timeout=10)
        countries_response.raise_for_status()
        countries_data = countries_response.json()

    except requests.exceptions.RequestException:
        raise ExternalAPIError("restcountries.com")
    
    print(f"Processing {len(countries_data)} countries...")
    for country_data in countries_data:
        currency_code = None
        exchange_rate = None
        estimated_gdp = None

        currencies = country_data.get('currencies')
        if currencies and isinstance(currencies, list) and len(currencies) > 0:
            currency_code = currencies[0].get('code')

            if currency_code:
                exchange_rate = rates.get(currency_code)

        population = country_data.get('population')
        if population and exchange_rate:
            random_multiplier = random.uniform(1000, 2000)
            estimated_gdp = (population * random_multiplier) / exchange_rate
        elif currency_code is None:
            estimated_gdp = 0

        Country.objects.update_or_create(
            name=country_data.get('name'),
            defaults={
                'capital': country_data.get('capital'),
                'region': country_data.get('region'),
                'population': population or 0,
                'flag_url': country_data.get('flag'),
                'currency_code': currency_code,
                'exchange_rate': exchange_rate,
                'estimated_gdp': estimated_gdp,
            }
        )

    total_countries = Country.objects.count()
    status_obj, created = Status.objects.update_or_create(
        pk=1,
        defaults={
            'total_countries': total_countries,
            'last_refreshed_at': datetime.now(timezone.utc)
        }
    )
    print("Database refresh complete!")

    top_5_gdp_countries = Country.objects.order_by('-estimated_gdp')[:5]

    generate_summary_image(
        total_countries=status_obj.total_countries,
        top_5_gdp=top_5_gdp_countries,
        last_refreshed_at=status_obj.last_refreshed_at
    )