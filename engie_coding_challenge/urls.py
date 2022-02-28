from django.urls import path
from productionplan.views import post_rest_api


urlpatterns = [
    path('productionplan/', post_rest_api),
    path('productionplan', post_rest_api),
]
