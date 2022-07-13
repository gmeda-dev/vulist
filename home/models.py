from django.db import models

class CVE(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=20, blank=False)

class Product(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=255, blank=False)

class Vulnerability(models.Model):
    id = models.CharField(primary_key=True, max_length=12, unique=True)
    title = models.CharField(max_length=255, blank=False)
    last_update = models.DateField(null=False)
    version = models.CharField(max_length=7, blank=False)
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    sector = models.CharField(max_length=128)

    products = models.ManyToManyField(Product)
    cve_ids = models.ManyToManyField(CVE)
