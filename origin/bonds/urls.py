from django.urls import path
from .views import GetBond


urlpatterns = [
    path('bonds/', GetBond.as_view(), name="bonds")
]
