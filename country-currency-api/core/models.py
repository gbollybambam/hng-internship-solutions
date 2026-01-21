from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    capital = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    population = models.BigIntegerField()
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    estimated_gdp = models.DecimalField(max_digits=30, decimal_places=4, null=True, blank=True)
    flag_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class Status(models.Model):
    last_refreshed_at = models.DateTimeField(null=True, blank=True)
    total_countries = models.IntegerField(default=0)

    def __str__(self):
        return f"Last refreshed at {self.last_refreshed_at}"

    class Meta:
        verbose_name_plural = "Status"