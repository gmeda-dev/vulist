from django.urls import path

from home.views import EditVulnerabilityView, IndexView

app_name = 'home'

urlpatterns = [
   path('', IndexView.as_view(), name='index'),
   path('<pk>/edit/', EditVulnerabilityView.as_view(), name='edit')
]