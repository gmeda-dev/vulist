from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from home.models import Product, Vulnerability

class IndexViewTests(TestCase):
    def setUp(self):
        pass

    def test_filtering(self):
        p = Product.objects.create(name='product AA')
        v1 = Vulnerability.objects.create(
            id='1',
            title='v1',
            last_update=timezone.now().date(),
            version='v1.5',
            cvss_score=9.0,
            sector='sector1'
        )
        v2 = Vulnerability.objects.create(
            id='2',
            title='v1',
            last_update=timezone.now().date(),
            version='v1.5',
            cvss_score=9.0,
            sector='sector1'
        )

        v1.products.add(p)
        v2.products.add(p)

        url = reverse('home:index')

        response = self.client.get(url, {'search': '', 'product_field_filter': p.name})

        self.assertEqual(response.context['all_vulnerabilities'].count(), 2)