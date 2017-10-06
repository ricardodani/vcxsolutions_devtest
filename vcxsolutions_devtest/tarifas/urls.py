from django.conf.urls import url
from tarifas.views import Home


urlpatterns = [
    url(r'^$', Home.as_view(), name='home')
]
