from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
from datetime import datetime, timezone
import requests

# Create your views here.
CAT_FACT_API_URL = "https://catfact.ninja/fact"
API_TIMEOUT = 5

def get_cat_fact():
    try:
        response = requests.get(CAT_FACT_API_URL, timeout=API_TIMEOUT)
        response.raise_for_status()

        data = response.json()
        return data.get("fact", "API returned data but no fact.")

    except requests.exceptions.Timeout:
        print("Cat Fact API request timed out.")
        return "The cat fact service timed out. (Fallback fact)"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cat fact: {e}")
        return "Could not fetch a cat fact due to network error. (Fallback fact)"

@require_GET
def profile_endpoint(request):

    fact = get_cat_fact()

    now_utc = datetime.now(timezone.utc)
    timestamp_iso = now_utc.isoformat().replace('+00:00', 'Z')

    response_data = {
        "status": "success",
        "user": {
            "email": settings.MY_EMAIL,
            "name": settings.MY_NAME,
            "stack": settings.MY_STACK
        },
        "timestamp": timestamp_iso,
        "fact": fact
    }

    return JsonResponse(response_data, status=200)
