from django.conf.urls import url,include
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),
    url(r'^auth/$',views.viewAuth),
    url(r'^login/$',views.viewLogin),
    url(r'^logoff/$',views.viewLogoff),
    url(r'^excluir/endereco/?$',views.excluirEndereco),
    url(r'^excluir/contato/?$',views.excluirContato),
    url(r'^excluir/entidade/?$',views.excluirEntidade),    
    url(r'^adicionar/fornecedor/?$',views.fornecedores),
    url(r'^fornecedor/?$',views.fornecedores),
    url(r'^buscar/fornecedor/?$',views.buscarFornecedores),
    url(r'^adicionar/produto/?$',views.produto),
    url(r'^produto/?$',views.produto),
    url(r'^buscar/produto/?$',views.buscarProduto),
    url(r'^cliente/?$',views.clientes),
    url(r'^buscar/cliente/?$',views.buscarClientes),
    url(r'^adicionar/cliente/?$',views.clientes),
    url(r'^buscar/produto_fornecedor/?$',views.buscarFornecedorProduto),
    url(r'^produto/buscar/marca/?$',views.buscarMarca),
    url(r'^buscar/historicoProduto/?$',views.buscarHistoricoProduto),
    url(r'^usuario/?$',views.usuario),
    url(r'^adicionar/usuario/?$',views.usuario),
    url(r'^buscar/usuario/?$',views.buscarUsuario),
    url(r'^excluir/usuario/?$',views.excluirUsuario),   
    url(r'^compra/?$',views.compras),
    url(r'^adicionar/compra/?$',views.compras),
    url(r'^buscar/compra/?$',views.buscarCompra),
    url(r'^excluir/compra/?$',views.excluirCompra),
    url(r'^adicionar/funcionario/?$',views.funcionarios),
    url(r'^funcionario/?$',views.funcionarios),
    url(r'^buscar/funcionario/?$',views.buscarFuncionario),
    url(r'^saida/?$',views.saidas),
    url(r'^adicionar/saida/?$',views.saidas),
    url(r'^buscar/saida/?$',views.buscarSaida),
    url(r'^excluir/saida/?$',views.excluirSaida),
]