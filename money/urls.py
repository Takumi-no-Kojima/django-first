from django.urls import path
from . import views
app_name = 'money'
urlpatterns = [
        path('', views.MainView.as_view(), name='index'),
        path('<int:year>/<int:month>', views.MainView.as_view(), name='index'),
        ]