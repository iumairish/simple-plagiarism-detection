from django.urls import path
from .views import HomeView

app_name = "splash"

urlpatterns = [
  path('', HomeView.as_view(), name='splash')
]
