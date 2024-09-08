from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imprimir', views.imprimir_orcamento, name='imprimir_orcamento'),
    # path('teste/', views.teste, name='teste'),
]