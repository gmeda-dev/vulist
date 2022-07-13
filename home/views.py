from django.views import View
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Case, When, Exists, OuterRef, ExpressionWrapper, BooleanField
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import  ListView 
from home.forms import EditVulnerabilityForm, FilterQueryForm, MarkVulnerabilityForm
from home.models import Vulnerability

from home.serializers import VulnerabilitySerializer


class IndexView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'home.html'

    def get_queryset(self):
        search = self.request.GET.get('search')
        product = self.request.GET.get('product_field_filter')

        all_vulnerabilities = Vulnerability.objects.all()

        if search:
            all_vulnerabilities = all_vulnerabilities.filter(Q(id__icontains=search) | Q(title__icontains=search))

        if product:
            all_vulnerabilities = all_vulnerabilities.filter(products=product)

        all_vulnerabilities = all_vulnerabilities.annotate(
            seen=Case(
                When(last_update__lt=(
                    self.request.user.previous_login if 
                        self.request.user.previous_login 
                        else Vulnerability.objects.latest('last_update').last_update),
                    then=True
                ),
                default=False
            )
        ).annotate(
            marked=Exists(Vulnerability.objects.filter(id=OuterRef('id'), user=self.request.user))
        ).order_by('-last_update')

        return all_vulnerabilities

        
    def get_context_data(self):
        self.object_list = self.get_queryset()
        context = super().get_context_data()
        context['filter_form'] = FilterQueryForm()
        context['mark_vulnerability_form'] = MarkVulnerabilityForm()

        return context

    def get(self, request):
        # if db is empty fetch data & populate db
        if Vulnerability.objects.count() == 0:
            response = requests.get('https://cert-portal.siemens.com/productcert/json/advisories.json')

            data = json.loads(response.content)

            serializer = VulnerabilitySerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        #############################
        return render(request, self.template_name, self.get_context_data())

    def post(self,request):
        form = MarkVulnerabilityForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get('value'):
                # need to add
                request.user.marked_vulnerabilities.add(form.cleaned_data['vulnerability'])
            else:
                # remove from marked vulnerabilities
                request.user.marked_vulnerabilities.remove(form.cleaned_data['vulnerability'])
            
        return render(request, self.template_name, self.get_context_data())


class EditVulnerabilityView(LoginRequiredMixin, View):
    form_class = EditVulnerabilityForm
    template_name = 'edit.html'

    def get_context_data(self, pk):
        vulnerability = get_object_or_404(Vulnerability, pk=pk)
        context = dict()
        context["form"] = self.form_class(instance=vulnerability)
        return context

    def get(self, request, pk):
        return render(request, self.template_name, self.get_context_data(pk))

    def post(self, request, pk):
        vulnerability = get_object_or_404(Vulnerability, pk=pk)
        form = self.form_class(request.POST, instance=vulnerability)

        if form.is_valid():
            return redirect('home:index')

        context = self.get_context_data(pk)
        context['form'] = form
        return render(request, self.template_name, context)