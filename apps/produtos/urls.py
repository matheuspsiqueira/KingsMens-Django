from django.urls import path
from . import views

urlpatterns = [
    path('cad_produtos', views.cad_produtos, name='cad_produtos'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrinho', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('aumenta_item/<int:item_id>/', views.aumenta_item, name='aumenta_item'),
    path('diminui_item/<int:item_id>/', views.diminui_item, name='diminui_item'),
    path('excluir_do_carrinho/<int:item_id>/', views.excluir_do_carrinho, name='excluir_do_carrinho'),
]