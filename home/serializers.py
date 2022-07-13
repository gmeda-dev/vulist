from home.models import CVE, Product, Vulnerability
from django.core.validators import EMPTY_VALUES
from rest_framework.serializers import ModelSerializer

class CVESerializer(ModelSerializer):
    class Meta:
        model = CVE
        fieds = ['id']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fieds = ['name']


class VulnerabilitySerializer(ModelSerializer):
    products = ProductSerializer(many=True)
    cve_ids = CVESerializer(many=True)

    class Meta:
        model = Vulnerability
        fields = [
            'id',
            'title',
            'last_update',
            'version',
            'cvss_score',
            'sector',
            'products',
            'cve_ids',
        ]

    def to_internal_value(self, data):
        new_data = {
            'id': data.get('id'),
            'title': data.get('title'),
            'last_update': data.get('last_update'),
            'version': data.get('document_version'),
            'sector': data.get('sector') if type(data.get('sector'))  == str else data.get('sector')[0],
            'cve_ids': data.get('cve-ids'),
            'cvss_score': 0 if data.get('cvss_score') in EMPTY_VALUES or data.get('cvss_score') == '' else data.get('cvss_score'),
            'products': data.get('products')
        }

        return new_data

    def create(self, validated_data):
        cves_list = []
        product_list = []
        for cve_id in validated_data['cve_ids']:
            cve, _ = CVE.objects.get_or_create(
                id=cve_id, defaults={'id': cve_id}
            )
            cves_list.append(cve)

        for product_str in validated_data['products']:
            product_obj, _ = Product.objects.get_or_create(
                name=product_str, defaults={'name': product_str}
            )
            product_list.append(product_obj)

        validated_data.pop('products')
        validated_data.pop('cve_ids')

        vulnerability, _ = Vulnerability.objects.update_or_create(
            id=validated_data['id'], defaults={**validated_data}
        )

        vulnerability.products.set(product_list)
        vulnerability.cve_ids.set(cves_list)

        return vulnerability