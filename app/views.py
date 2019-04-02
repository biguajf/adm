from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_mongoengine.mongo_auth import *
from django.middleware.csrf import _get_new_csrf_string as _get_new_csrf_key, get_token 

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django_mongoengine import Document, DynamicDocument, EmbeddedDocument, fields
from django.middleware.csrf import get_token
import json
from ast import literal_eval
from app.models import *
from mongoengine.queryset.visitor import Q

#Funções
def atualizarEstoque(tipo, produto, fornecedor):
  if tipo == 'compra':
    entidade = Entidade.objects(id=fornecedor)[0]
    fornecedor_produto = json.loads(produto)
    for i in fornecedor_produto:
      n = 0
      produto_split = i['produto']
      a,b = produto_split.split('  - ')
      for j in entidade.produtos:
        if a == j['produto_nome'] and b == j['marca']:        
          entidade.produtos[n]['preco'] = i['preco_unitario']
          entidade.save() #salva no fornecedor
          #salva no produto
          produto_save = Entidade.objects(id=j['_id'])[0]
          m=0
          for k in produto_save.detalhes.fornecedor:
            if k['_id'] == fornecedor:
              detalhes = produto_save.detalhes
              detalhes['fornecedor'][m]['preco'] = i['preco_unitario']
              detalhes['estoque_atual'] = str(float(detalhes['estoque_atual']) + float(i['quantidade']))
              produto_save.detalhes = detalhes
              produto_save.update(detalhes = detalhes)
              produto_save.save(commit = True)
            m+=1
        n+=1
    return
  elif tipo == 'saida':
    fornecedor_produto = produto
    for i in fornecedor_produto:
      produto_split = i['produto']
      a,b = produto_split.split('  - ')
      produto_saida = Entidade.objects(Q(tipo = 'PRODUTO') & Q(nome=a) & Q(detalhes__marca=b))[0]
      detalhes = produto_saida.detalhes
      detalhes['estoque_atual'] = str(float(detalhes['estoque_atual']) - float(i['quantidade']))
      produto_saida.detalhes = detalhes
      produto_saida.update(detalhes = detalhes)
    return
  else:
    return

#Autentivcacao
def viewLogin(request):
  if not request.user.is_authenticated:
    template ='app/login.html'
    token = get_token(request)
    params ={'token' : token}
    return render(request,template,params)
  else:
    return redirect('/')

def viewAuth(request):
  username = request.POST['username'].upper()
  password = request.POST['password']
  user = authenticate(request, username=username, password=password.encode('utf8'))
  if user and user.is_active:
    if user.check_password(password):
      login(request,user)
      token = _get_new_csrf_key()
      if not request.session.session_key:
        request.session.save()
      return redirect('/')
    else:
      return redirect('/login/')
  else:
    return redirect('/login/')

def viewLogoff(request):
  logout(request)
  return redirect('/login/')

######
 
@login_required(login_url='/login/')
def index(request):
    permissoes =  request.user.user_permissions[0].id
    username = request.user.username
    context = literal_eval(permissoes)
    context['username'] = username
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def usuario(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['usuario'] == 1 :
      try:
        idUsuario = request.POST['usuario[id]']
      except:
        idUsuario = '0'
        pass
      #   
      if idUsuario == '0':
        usuario = Usuario()
        usuario.nome             = request.POST['usuario[nome]']
        usuario.usuario          = request.POST['usuario[usuario]']
        usuario.senha            = request.POST['usuario[senha]']
        usuario.email            = request.POST['usuario[email]']
        usuario.user_permissions = request.POST['usuario[permissoes]']
        #
        usuario.save(commit = True)
        #
        result={'result':1}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
      else:      
        usuario = Usuario.objects(id = idUsuario)[0]
        usuario.nome            = request.POST['usuario[nome]']
        usuario.usuario         = request.POST['usuario[usuario]']
        usuario.senha           = request.POST['usuario[senha]']
        usuario.email           = request.POST['usuario[email]']
        usuario.user_permissions = request.POST['usuario[permissoes]']   
        #
        usuario.save(commit = True)
        result={'result':1}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

    else:
            result={'result':0}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
  else:
    template = loader.get_template('app/usuario.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def excluirUsuario(request):  
  template ='usuarios.html'
  token = get_token(request)  
  if request.method == 'POST':
    permissoes =  request.user.user_permissions[0].id
    context = literal_eval(permissoes)
    if context['usuario'] == 1 :
      idUsuario = request.POST['id']
      usuarioSelect = Usuario.objects(id=idUsuario)[0]
      usuarioSelect.delete()
    #
    result={'result':'/cadastros/usuarios/'}
    return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json')


@login_required(login_url='/login/')
def buscarUsuario(request):
  if 'id' in request.GET:
    usuario = Usuario.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    usuario = Usuario.objects(tipo = 'FORNECEDOR')
  else:
    filtro = request.GET['filtro']
    usuario = Usuario.objects(Q(nome__icontains=filtro) | Q(nome_usuario=filtro))

  data = []
  for row in usuario:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def gentella_html(request):
  if request.method == 'POST':
      usuario = Usuario()
      usuario.nome = request.POST['cliente']  
      #      
      usuario.save(commit = True)  

      result={'result':'1'}
      return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

  token = get_token(request)
  context = {'token':token}
  load_template = request.path.split('/')[-1]
  template = loader.get_template('app/' + load_template)
  return HttpResponse(template.render(context, request))



@login_required(login_url='/login/')
def excluirEntidade(request):
  if request.method =='POST':
    permissoes =  request.user.user_permissions[0].id
    context = literal_eval(permissoes)
    entidade = Entidade.objects(id=request.POST['id'])
    if entidade[0]['tipo'] == 'PRODUTO':
      if context['produto'] == 1 :
      #Se a entidade for um produto
        for row in entidade[0]['detalhes']['fornecedor']: #busca todos os fornecedores daquele produto
          fornecedor = Entidade.objects(id=row['_id'])
          for produto_i in fornecedor[0]['produtos']: # busca todos os produtos do fornecedor
            print(produto_i)
            if produto_i['produto_nome'] == entidade[0]['nome'] and produto_i['marca'] == entidade[0]['detalhes']['marca']: #procura o produto que será excluido
              fornecedor.update(pull__produtos = produto_i) #apaga o produto do fornecedor
        entidade.delete()
        result = {'result':1}
      else:
        result = {'result': 0}

    elif entidade[0]['tipo'] == 'CLIENTE':
      if context['cliente'] == 1 :
        entidade.delete()
        result = {'result': 1}
      else:
        result = {'result': 0}

    elif entidade[0]['tipo'] == 'FORNECEDOR':
      if context['fornecedor'] == 1 :
        entidade.delete()
        result = {'result': 1}
      else:
        result = {'result': 0}

    elif entidade[0]['tipo'] == 'FUNCIONARIO':
      if context['funcionario'] == 1 :
        entidade.delete()
        result = {'result': 1}
      else:
        result = {'result': 0}
    else:
      result = {'result': 0}

    return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json') 

@login_required(login_url='/login/')
def fornecedores(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['fornecedor'] == 1 :
      if 'fornecedor[tipo_pessoa]' in request.POST:
        id_entidade = request.POST['fornecedor[id_fornecedor]']

        if id_entidade == '0': #novo
          entidade = Entidade()
        else: #editar
          entidade = Entidade.objects(id=id_entidade)[0]
        
        value_ativo = request.POST['fornecedor[ativo]']
        if value_ativo == 'true':
          entidade.ativo = True
        elif value_ativo == 'false':
          entidade.ativo = False
        
        if request.POST['fornecedor[tipo_pessoa]'] :
          entidade.tipo_pessoa = request.POST['fornecedor[tipo_pessoa]']
        
        if request.POST['fornecedor[nome]'] :
          entidade.nome = request.POST['fornecedor[nome]']

        entidade.observacao = request.POST['fornecedor[observacao]']

        #PJ
        if request.POST['fornecedor[tipo_pessoa]'] == 'PJ':
          if request.POST['fornecedor[CNPJ]'] :
            entidade.CNPJ = request.POST['fornecedor[CNPJ]']      
          
          if request.POST['fornecedor[nome_fantasia]'] :
            entidade.nome_fantasia = request.POST['fornecedor[nome_fantasia]']
          
          if request.POST['fornecedor[inscricao_estadual]'] :
            entidade.inscricao_estadual = request.POST['fornecedor[inscricao_estadual]']
          
          if request.POST['fornecedor[inscricao_municipal]'] :
            entidade.inscricao_municipal = request.POST['fornecedor[inscricao_municipal]']
          
          if request.POST['fornecedor[data_fundacao]'] :
            entidade.data_fundacao = datetime.datetime.strptime(request.POST['fornecedor[data_fundacao]'], "%d/%m/%Y").date()
          
          if request.POST['fornecedor[CRT]'] :
            entidade.CRT = request.POST['fornecedor[CRT]']
        #PF      
        if request.POST['fornecedor[tipo_pessoa]'] == 'PF':
          if request.POST['fornecedor[CPF]'] :
            entidade.CPF = request.POST['fornecedor[CPF]']
          
          if request.POST['fornecedor[RG]'] :
            entidade.RG = request.POST['fornecedor[RG]']
          
          if request.POST['fornecedor[data_nascimento]'] :
            entidade.data_nascimento = datetime.datetime.strptime(request.POST['fornecedor[data_nascimento]'] , "%d/%m/%Y").date()
          
          if request.POST['fornecedor[sexo]'] :
            entidade.sexo = request.POST['fornecedor[sexo]']
          
          if request.POST['fornecedor[estado_civil]'] :
            entidade.estado_civil = request.POST['fornecedor[estado_civil]']

        fornecedor = Fornecedor()
        if request.POST['fornecedor[produto]'] :
          fornecedor_produto = json.loads(request.POST['fornecedor[produto]'])
          entidade.produtos = fornecedor_produto
        entidade.tipo = 'FORNECEDOR'
        entidade.save(commit = True)
        id_gerado = str(entidade.id)

        if request.POST['fornecedor[produto]'] :
          fornecedor_produto = json.loads(request.POST['fornecedor[produto]'])        
          for produtos in fornecedor_produto: #Varre todos os produtos de cada fornecedor     
            produto_in_fornecedor = []
            produto_fornecedor = Entidade.objects(id=produtos['_id'])
            produto_in_fornecedor = list((produto_fornecedor).aggregate(
                      { "$unwind": "$detalhes.fornecedor" },
                      {"$group": {
                          "_id": "$_id",
                          "username": { 
                            "$push": {           
                                        "$cond":[
                                            {"$eq": [ "$detalhes.fornecedor.nome", request.POST['fornecedor[nome]'] ]},
                                            {"fornecedor": "$detalhes.fornecedor.nome"},
                                            'null'
                                        ]                        
                                    } 
                          }
                        }
                      },
                      {
                          "$project": {
                              "fornecedor":{"$setDifference":["$username", ['null']]}
                          }
                      }
                    ))# Se vazio não tem o produto criado neste fornecedor
            produto_save = produto_fornecedor[0]
            if produto_in_fornecedor:
              if not produto_in_fornecedor[0]['fornecedor']:
                str_produto = '{"_id" : "'+id_gerado+'", "nome" : "'+request.POST['fornecedor[nome]']+'", "preco":"'+produtos['preco']+'"}'
                json_produtos = json.loads(str_produto)
                produto_fornecedor.update(push__detalhes__fornecedor = json_produtos) #resolver push para su documment
              else:
                entidade_s = Entidade.objects(id=produtos['_id'])[0] 
                j = 0
                for i in entidade_s.detalhes.fornecedor:
                  if i['_id'] == id_entidade:
                    produto = Produto()
                    produto.preco = produtos['preco']
                    produto._id = id_entidade
                    produto.nome = request.POST['fornecedor[nome]']
                    entidade_s.detalhes.fornecedor[j] = produto
                    entidade_s.save()
                  j += 1
            else:
              str_produto = '{"_id" : "'+id_gerado+'", "nome" : "'+request.POST['fornecedor[nome]']+'", "preco":"'+produtos['preco']+'"}'
              json_produtos = json.loads(str_produto)
              produto_fornecedor.update(push__detalhes__fornecedor = json_produtos)


        result = {'result': id_gerado}
        return HttpResponse(json.dumps(result, ensure_ascii=False),
            content_type='application/json')
      elif 'contato[nome]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_contato   = int(request.POST['contato[id_contato]'])
          #
          params={'nome': request.POST['contato[nome]'], 'email' : request.POST['contato[email]'], 'telefone' : request.POST['contato[telefone]']}       

          if id_contato > 0: # editar
            entidade = Entidade.objects(id=id_entidade)[0]
            entidade.contato[id_contato-1].nome     = request.POST['contato[nome]']
            entidade.contato[id_contato-1].email    = request.POST['contato[email]']
            entidade.contato[id_contato-1].telefone = request.POST['contato[telefone]']
            entidade.save()
          else: # criar novo
            send = Entidade.objects(id=id_entidade).update(push__contato = params)

          result = {'result': 1} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result': 0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')

      elif 'endereco[logradouro]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_endereco   = int(request.POST['endereco[id_endereco]'])
          params={'logradouro': request.POST['endereco[logradouro]'], 'cidade' : request.POST['endereco[cidade]'], 'numero' : request.POST['endereco[numero]'], 'estado' : request.POST['endereco[estado]'] , 'CEP' : request.POST['endereco[CEP]'], 'tipo_logradouro' : request.POST['endereco[tipoLogradouro]'], 'tipo' : request.POST['endereco[tipo]'], 'bairro' : request.POST['endereco[bairro]'], 'complemento' : request.POST['endereco[complemento]'], 'referencia' : request.POST['endereco[referencia]']}
          if id_endereco > 0:
            empresa = Entidade.objects(id=id_entidade)[0]
            empresa.endereco[id_endereco-1].logradouro       = request.POST['endereco[logradouro]']
            empresa.endereco[id_endereco-1].cidade           = request.POST['endereco[cidade]']
            empresa.endereco[id_endereco-1].numero           = request.POST['endereco[numero]']
            empresa.endereco[id_endereco-1].estado           = request.POST['endereco[estado]']
            empresa.endereco[id_endereco-1].CEP              = request.POST['endereco[CEP]']
            empresa.endereco[id_endereco-1].tipo_logradouro  = request.POST['endereco[tipoLogradouro]']
            empresa.endereco[id_endereco-1].tipo             = request.POST['endereco[tipo]']
            empresa.endereco[id_endereco-1].complemento      = request.POST['endereco[complemento]']
            empresa.endereco[id_endereco-1].bairro           = request.POST['endereco[bairro]']
            empresa.endereco[id_endereco-1].referencia       = request.POST['endereco[referencia]']
            empresa.save()
          else:
            send = Entidade.objects(id=id_entidade).update(push__endereco = params)
          result = {'result': 1, 'params':params, 'id_entidade': id_entidade} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result': 0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
    else:
      result = {'result': 0} 
      return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
  else:
    template = loader.get_template('app/fornecedores.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarFornecedores(request):
  if 'id' in request.GET:
    fornecedores = Entidade.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    fornecedores = Entidade.objects(tipo = 'FORNECEDOR')
  else:
    filtro = request.GET['filtro']
    fornecedores = Entidade.objects(Q(tipo = 'FORNECEDOR') & (Q(nome__icontains=filtro) | Q(nome_fantasia__icontains=filtro) | Q(CNPJ=filtro)))

  data = []
  for row in fornecedores:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def produto(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['produto'] == 1 :    
      id_produto = request.POST['id_produto']
      produto_fornecedor = json.loads(request.POST['fornecedor'])
      if id_produto == '0': #novo
        entidade = Entidade()
        entidade.historico = True
      else: #editar
        entidade = Entidade.objects(id=id_produto)[0]      
        historico = HistoricoProduto.objects(Q(nome = request.POST['nome']) & Q(marca=request.POST['marca'])).order_by('-_id')[:1]
        entidade.historico = False
        for k in historico[0].fornecedor:
          for j in produto_fornecedor:
            if j['nome'] == k['nome']:
              if k['preco'] != j['preco']:
                entidade.historico = True
      
      if request.POST['nome'] :
        entidade.nome = request.POST['nome']

      entidade.ativo = True

      produto = Produto()
      produto.descricao = 'PRODUTO'
      if request.POST['nome'] :
        produto.produto_nome = request.POST['nome']

      if request.POST['codigo'] :
        produto.codigo = request.POST['codigo']
      
      if request.POST['unidade'] :
        produto.unidade = request.POST['unidade']

      if request.POST['estoque_minimo'] :
        produto.estoque_minimo = request.POST['estoque_minimo']

      if request.POST['estoque_atual'] :
        produto.estoque_atual = request.POST['estoque_atual']

      if request.POST['marca'] :
        produto.marca = request.POST['marca']

      if request.POST['fornecedor'] :
        produto.fornecedor = produto_fornecedor


      entidade.tipo = 'PRODUTO'
      entidade.detalhes = produto
      entidade.save()
      id_gerado = str(entidade.id)
      produto._id = id_gerado
      for fornecedores in produto_fornecedor: #Varre todos os produtos de cada fornecedor
        fornecedor_in_produto = []
        fornecedor_produto = Entidade.objects(id=fornecedores['_id'])
        fornecedor_in_produto = list((fornecedor_produto).aggregate(
                  { "$unwind": "$produtos" },
                  {"$group": {
                      "_id": "$_id",
                      "username": { 
                        "$push": {
                                  "$cond":[{
                                    "$and": [          
                                        {"$eq": [ "$produtos.produto_nome", request.POST['nome'] ]},
                                        {"$eq": [ "$produtos.marca", request.POST['marca'] ]}
                                    ]},
                                        {"produto": "$produtos.produto_nome"},
                                        'null'
                                  ]         
                                } 
                      }
                    }
                  },
                  {
                      "$project": {
                          "produto":{"$setDifference":["$username", ['null']]}
                      }
                  }
                ) )# Se vazio não tem o produto criado neste fornecedor
        if fornecedor_in_produto:
          if not fornecedor_in_produto[0]['produto']:
            str_produto = '{"produto_nome" : "'+ request.POST['nome'] +'", "_id" : "'+id_gerado+'","preco":"'+fornecedores['preco']+'","marca":"'+request.POST['marca']+'"}'
            json_produtos = json.loads(str_produto)
            fornecedor_produto.update(push__produtos = json_produtos)
          else:
            entidade_s = Entidade.objects(id=fornecedores['_id'])[0] 
            j = 0
            for i in entidade_s.produtos:
              if i['_id'] == id_produto:
                entidade_s.produtos[j]['produto_nome'] = request.POST['nome']
                entidade_s.produtos[j]['preco']        = fornecedores['preco']
                entidade_s.produtos[j]['marca']        = request.POST['marca']
                entidade_s.save()
              j += 1
        else:
          print('entrou')
          str_produto = '{"produto_nome" : "' + request.POST['nome'] + '", "_id" : "'+id_gerado+'","preco":"'+fornecedores['preco']+'","marca":"'+request.POST['marca']+'"}'
          json_produtos = json.loads(str_produto)
          fornecedor_produto.update(push__produtos = json_produtos)

      result = {'result': id_gerado}
      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')
    else:
      result = {'result': 0}
      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')
  else:
    template = loader.get_template('app/produtos.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarProduto(request):
  if 'id' in request.GET:
    produto = Entidade.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    produto = Entidade.objects(tipo = 'PRODUTO')
  else:
    filtro = request.GET['filtro']
    produto = Entidade.objects(Q(tipo = 'PRODUTO') & Q(nome__icontains=filtro))

  data = []
  for row in produto:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def buscarMarca(request):
  if 'id' in request.GET:
    marca = Marca.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    marca = Marca.objects()
  else:
    filtro = request.GET['filtro']
    marca = Marca.objects(Q(nome__icontains=filtro))

  data = []
  for row in marca:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def buscarFornecedorProduto(request):
  if 'id' in request.GET:
    fornecedor = Entidade.objects(id=request.GET['id'])[0]
    produtos_id = []
    for produto in fornecedor.produtos:
      produtos_id.append(produto['_id'])

    produto = Entidade.objects(id__in = produtos_id)
    data = []
    for row in produto:
      for forne in row['detalhes']['fornecedor']:
        if forne['_id'] == request.GET['id']:
          val = { 'nome' : row['nome'], 'codigo' : row['detalhes']['codigo'], 'unidade' : row['detalhes']['unidade'], 'preco' : forne['preco'], 'marca' : row['detalhes']['marca']}
          data.append(val)
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def excluirProduto(request):
  if request.method =='POST':
    permissoes =  request.user.user_permissions[0].id
    context = literal_eval(permissoes)
    if context['produto'] == 1 :
      produto = Entidade.objects(id=request.POST['id'])
      produto.delete()
      result = {'result':'1'}
      return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json')
    else:
      result = {'result':'0'}
      return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def excluirEndereco(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method =='POST':
    try:
      id_entidade = request.POST['entidade']
      idDel = int(request.POST['deletar[idDel]'])
      fornecedor = Entidade.objects(id=id_entidade)[0]
      if fornecedor[0]['tipo'] == 'PRODUTO':
        if context['produto'] == 1 :
          fornecedor.update(pull__endereco = fornecedor.endereco[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0]['tipo'] == 'CLIENTE':
        if context['cliente'] == 1 :
          fornecedor.update(pull__endereco = fornecedor.endereco[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0]['tipo'] == 'FORNECEDOR':
        if context['fornecedor'] == 1 :
          fornecedor.update(pull__endereco = fornecedor.endereco[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0]['tipo'] == 'FUNCIONARIO':
        if context['funcionario'] == 1 :
          fornecedor.update(pull__endereco = fornecedor.endereco[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}
      else:
        result = {'result': 0}

      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')
    except:
      result = {'result': 0} 
      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')

@login_required(login_url='/login/')
def excluirContato(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    try:
      id_entidade = request.POST['entidade']
      idDel = int(request.POST['deletar[idDel]'])
      fornecedor = Entidade.objects(id=id_entidade)[0]
      if fornecedor[0]['tipo'] == 'PRODUTO':
        if context['produto'] == 1 :
          fornecedor.update(pull__contato = fornecedor.contato[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0]['tipo'] == 'CLIENTE':
        if context['cliente'] == 1 :
          fornecedor.update(pull__contato = fornecedor.contato[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0][tipo] == 'FORNECEDOR':
        if context['fornecedor'] == 1 :
          fornecedor.update(pull__contato = fornecedor.contato[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}

      elif fornecedor[0]['tipo'] == 'FUNCIONARIO':
        if context['funcionario'] == 1 :
          fornecedor.update(pull__contato = fornecedor.contato[idDel-1])
          result = {'result': 1}
        else:
          result = {'result': 0}
      else:
        result = {'result': 0}

      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')
    except:
      result = {'result': 0} 
      return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')

@login_required(login_url='/login/')
def buscarClientes(request):
  if 'id' in request.GET:
    cliente = Entidade.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    cliente = Entidade.objects( tipo = 'CLIENTE')
  else:
    filtro = request.GET['filtro']
    cliente = Entidade.objects(Q(tipo = 'CLIENTE') & (Q(nome__icontains=filtro) | Q(nome_fantasia__icontains=filtro) | Q(CNPJ=filtro)))

  data = []
  for row in cliente:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def clientes(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['cliente'] == 1 :
      if 'cliente[tipo_pessoa]' in request.POST:
        id_entidade = request.POST['cliente[id_cliente]']

        if id_entidade == '0': #novo
          entidade = Entidade()
        else: #editar
          entidade = Entidade.objects(id=id_entidade)[0]
        
        value_ativo = request.POST['cliente[ativo]']
        if value_ativo == 'true':
          entidade.ativo = True
        elif value_ativo == 'false':
          entidade.ativo = False
        
        if request.POST['cliente[tipo_pessoa]'] :
          entidade.tipo_pessoa = request.POST['cliente[tipo_pessoa]']
        
        if request.POST['cliente[nome]'] :
          entidade.nome = request.POST['cliente[nome]']

        entidade.observacao = request.POST['cliente[observacao]']

        #PJ
        if request.POST['cliente[tipo_pessoa]'] == 'PJ':
          if request.POST['cliente[CNPJ]'] :
            entidade.CNPJ = request.POST['cliente[CNPJ]']      
          
          if request.POST['cliente[nome_fantasia]'] :
            entidade.nome_fantasia = request.POST['cliente[nome_fantasia]']
          
          if request.POST['cliente[inscricao_estadual]'] :
            entidade.inscricao_estadual = request.POST['cliente[inscricao_estadual]']
          
          if request.POST['cliente[inscricao_municipal]'] :
            entidade.inscricao_municipal = request.POST['cliente[inscricao_municipal]']
          
          if request.POST['cliente[data_fundacao]'] :
            entidade.data_fundacao = datetime.datetime.strptime(request.POST['cliente[data_fundacao]'], "%d/%m/%Y").date()
          
          if request.POST['cliente[CRT]'] :
            entidade.CRT = request.POST['cliente[CRT]']
        #PF      
        if request.POST['cliente[tipo_pessoa]'] == 'PF':
          if request.POST['cliente[CPF]'] :
            entidade.CPF = request.POST['cliente[CPF]']
          
          if request.POST['cliente[RG]'] :
            entidade.RG = request.POST['cliente[RG]']
          
          if request.POST['cliente[data_nascimento]'] :
            entidade.data_nascimento =  datetime.datetime.strptime(request.POST['cliente[data_nascimento]'], "%d/%m/%Y").date()
          
          if request.POST['cliente[sexo]'] :
            entidade.sexo = request.POST['cliente[sexo]']
          
          if request.POST['cliente[estado_civil]'] :
            entidade.estado_civil = request.POST['cliente[estado_civil]']

          if request.POST['cliente[nome_conjuge]'] :
            entidade.nome_conjuge = request.POST['cliente[nome_conjuge]']
          
        cliente = Cliente()
        entidade.tipo = 'CLIENTE'
        entidade.descricao = cliente
        entidade.save(commit = True)
        id_gerado = str(entidade.id)

        result = {'result': id_gerado}
        return HttpResponse(json.dumps(result, ensure_ascii=False),
            content_type='application/json')
      elif 'contato[nome]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_contato   = int(request.POST['contato[id_contato]'])
          #
          params={'nome': request.POST['contato[nome]'], 'email' : request.POST['contato[email]'], 'telefone' : request.POST['contato[telefone]']}       

          if id_contato > 0: # editar
            entidade = Entidade.objects(id=id_entidade)[0]
            entidade.contato[id_contato-1].nome     = request.POST['contato[nome]']
            entidade.contato[id_contato-1].email    = request.POST['contato[email]']
            entidade.contato[id_contato-1].telefone = request.POST['contato[telefone]']
            entidade.save()
          else: # criar novo
            send = Entidade.objects(id=id_entidade).update(push__contato = params)

          result = {'result': 1} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result': 0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')

      elif 'endereco[logradouro]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_endereco   = int(request.POST['endereco[id_endereco]'])
          params={'logradouro': request.POST['endereco[logradouro]'], 'cidade' : request.POST['endereco[cidade]'], 'numero' : request.POST['endereco[numero]'], 'estado' : request.POST['endereco[estado]'] , 'CEP' : request.POST['endereco[CEP]'], 'tipo_logradouro' : request.POST['endereco[tipoLogradouro]'], 'tipo' : request.POST['endereco[tipo]'], 'bairro' : request.POST['endereco[bairro]'], 'complemento' : request.POST['endereco[complemento]'], 'referencia' : request.POST['endereco[referencia]']}
          if id_endereco > 0:
            empresa = Entidade.objects(id=id_entidade)[0]
            empresa.endereco[id_endereco-1].logradouro       = request.POST['endereco[logradouro]']
            empresa.endereco[id_endereco-1].cidade           = request.POST['endereco[cidade]']
            empresa.endereco[id_endereco-1].numero           = request.POST['endereco[numero]']
            empresa.endereco[id_endereco-1].estado           = request.POST['endereco[estado]']
            empresa.endereco[id_endereco-1].CEP              = request.POST['endereco[CEP]']
            empresa.endereco[id_endereco-1].tipo_logradouro  = request.POST['endereco[tipoLogradouro]']
            empresa.endereco[id_endereco-1].tipo             = request.POST['endereco[tipo]']
            empresa.endereco[id_endereco-1].complemento      = request.POST['endereco[complemento]']
            empresa.endereco[id_endereco-1].bairro           = request.POST['endereco[bairro]']
            empresa.endereco[id_endereco-1].referencia       = request.POST['endereco[referencia]']
            empresa.save()
          else:
            send = Entidade.objects(id=id_entidade).update(push__endereco = params)
          result = {'result': 1, 'params':params, 'id_entidade': id_entidade} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result': 0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
    else:
      result = {'result': 0} 
      return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
  else:
    template = loader.get_template('app/clientes.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarHistoricoProduto(request):
  if request.method == 'GET':
    nome  = request.GET['nome']
    marca = request.GET['marca']
    historico = HistoricoProduto.objects(Q(nome = nome) & Q(marca=marca)).order_by('-_id')[:5]

    data = []
    for row in historico:
      data.append(json.loads(row.to_json()))
    #
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def compras(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['compra'] == 1 :
      id_compra = request.POST['id']
      if id_compra == '0': #novo
        compra = Compra()
      else: #editar
        compra = Compra.objects(id=id_compra)[0]

      fornecedor_produto   = Entidade.objects(id=request.POST['fornecedor'])[0]
      compra.fornecedor    = fornecedor_produto.nome
      compra.fornecedor_id = request.POST['fornecedor']
      compra.total         = request.POST['total']
      if request.POST['data_cadastro'] :
        compra.data_cadastro = datetime.datetime.strptime(request.POST['data_cadastro'], "%d/%m/%Y").date()
      compra.produtos      = json.loads(request.POST['produtos'])
      
      compra.save(commit = True)
      id_gerado = str(compra.id)
      result = {'result': id_gerado}
      atualizarEstoque('compra', request.POST['produtos'], request.POST['fornecedor'])
      return HttpResponse(json.dumps(result, ensure_ascii=False),
            content_type='application/json')
    else:
      result = {'result': 0}
      return HttpResponse(json.dumps(result, ensure_ascii=False),
            content_type='application/json')
  else:
    template = loader.get_template('app/compras.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarCompra(request):
  if request.method == 'GET':
    if 'id' in request.GET:
      compra = Compra.objects(id=request.GET['id'])
    elif 'mes' in request.GET:
      mes = datetime.datetime.strptime(request.GET['mes'], "%d/%m/%Y")
      if mes.month < 12:
        data_final = mes.replace(month=mes.month+1)
      else:
        data_final = mes.replace(month=1, year=mes.year+1)
      compra = Compra.objects(Q(data_cadastro__gte=mes) & Q(data_cadastro__lt=data_final))
    elif not 'filtro' in request.GET:
      compra = Compra.objects()
    else:
      filtro = request.GET['filtro']
      compra = Compra.objects(Q(fornecedor__icontains=filtro))

    data = []
    for row in compra:
      data.append(json.loads(row.to_json()))
    #
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def excluirCompra(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if context['compra'] == 1 :
    if request.method =='POST':
      compra = Compra.objects(id=request.POST['id'])
      compra.delete()
      result = {'result':1}
  else:
    result = {'result':0}
  return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def funcionarios(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['funcionario'] == 1 :
      if 'funcionario[tipo_pessoa]' in request.POST:
        id_entidade = request.POST['funcionario[id_funcionario]']

        if id_entidade == '0': #novo
          entidade = Entidade()
        else: #editar
          entidade = Entidade.objects(id=id_entidade)[0]
        
        value_ativo = request.POST['funcionario[ativo]']
        if value_ativo == 'true':
          entidade.ativo = True
        elif value_ativo == 'false':
          entidade.ativo = False
        
        if request.POST['funcionario[tipo_pessoa]'] :
          entidade.tipo_pessoa = request.POST['funcionario[tipo_pessoa]']
        if request.POST['funcionario[nome]'] :
          entidade.nome = request.POST['funcionario[nome]']
        entidade.observacao = request.POST['funcionario[observacao]']

        #PJ
        if request.POST['funcionario[tipo_pessoa]'] == 'PJ':
          if request.POST['funcionario[CNPJ]'] :
            entidade.CNPJ = request.POST['funcionario[CNPJ]']      
          if request.POST['funcionario[nome_fantasia]'] :
            entidade.nome_fantasia = request.POST['funcionario[nome_fantasia]']
          if request.POST['funcionario[inscricao_estadual]'] :
            entidade.inscricao_estadual = request.POST['funcionario[inscricao_estadual]']
          if request.POST['funcionario[inscricao_municipal]'] :
            entidade.inscricao_municipal = request.POST['funcionario[inscricao_municipal]']
          if request.POST['funcionario[data_fundacao]'] :
            entidade.data_fundacao = datetime.datetime.strptime(request.POST['funcionario[data_fundacao]'], "%d/%m/%Y").date()
          if request.POST['funcionario[CRT]'] :
            entidade.CRT = request.POST['funcionario[CRT]']
        #PF      
        if request.POST['funcionario[tipo_pessoa]'] == 'PF':
          if request.POST['funcionario[CPF]'] :
            entidade.CPF = request.POST['funcionario[CPF]']
          if request.POST['funcionario[RG]'] :
            entidade.RG = request.POST['funcionario[RG]']
          if request.POST['funcionario[registro]']:
            entidade.registro = request.POST['funcionario[registro]']
          if request.POST['funcionario[data_nascimento]'] :
            entidade.data_nascimento = datetime.datetime.strptime(request.POST['funcionario[data_nascimento]'] , "%d/%m/%Y").date()
          if request.POST['funcionario[sexo]'] :
            entidade.sexo = request.POST['funcionario[sexo]']        
          if request.POST['funcionario[estado_civil]'] :
            entidade.estado_civil = request.POST['funcionario[estado_civil]']
          if request.POST['funcionario[nome_pai]']:
            entidade.nome_pai = request.POST['funcionario[nome_pai]']
          if request.POST['funcionario[nome_mae]']:
            entidade.nome_mae = request.POST['funcionario[nome_mae]']
          if request.POST['funcionario[grau_instrucao]']:
            entidade.grau_instrucao = request.POST['funcionario[grau_instrucao]']
          if request.POST['funcionario[complemento_instrucao]']:
            entidade.complemento_instrucao = request.POST['funcionario[complemento_instrucao]']

        funcionario         = Funcionario()
        funcionario.cargo   = request.POST['funcionario[cargo]']
        funcionario.salario = request.POST['funcionario[salario]']
        entidade.tipo       = 'FUNCIONARIO'
        entidade.detalhes   = funcionario
        entidade.save(commit = True)
        id_gerado = str(entidade.id)
        result = {'result': id_gerado}
        return HttpResponse(json.dumps(result, ensure_ascii=False),
            content_type='application/json')

      elif 'contato[nome]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_contato   = int(request.POST['contato[id_contato]'])
          #
          params={'nome': request.POST['contato[nome]'], 'email' : request.POST['contato[email]'], 'telefone' : request.POST['contato[telefone]']}       

          if id_contato > 0: # editar
            entidade = Entidade.objects(id=id_entidade)[0]
            entidade.contato[id_contato-1].nome     = request.POST['contato[nome]']
            entidade.contato[id_contato-1].email    = request.POST['contato[email]']
            entidade.contato[id_contato-1].telefone = request.POST['contato[telefone]']
            entidade.save()
          else: # criar novo
            send = Entidade.objects(id=id_entidade).update(push__contato = params)

          result = {'result': 1} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result':0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')

      elif 'endereco[logradouro]' in request.POST:
        try:
          id_entidade  = request.POST['entidade']
          id_endereco   = int(request.POST['endereco[id_endereco]'])
          params={'logradouro': request.POST['endereco[logradouro]'], 'cidade' : request.POST['endereco[cidade]'], 'numero' : request.POST['endereco[numero]'], 'estado' : request.POST['endereco[estado]'] , 'CEP' : request.POST['endereco[CEP]'], 'tipo_logradouro' : request.POST['endereco[tipoLogradouro]'], 'tipo' : request.POST['endereco[tipo]'], 'bairro' : request.POST['endereco[bairro]'], 'complemento' : request.POST['endereco[complemento]'], 'referencia' : request.POST['endereco[referencia]']}
          if id_endereco > 0:
            empresa = Entidade.objects(id=id_entidade)[0]
            empresa.endereco[id_endereco-1].logradouro       = request.POST['endereco[logradouro]']
            empresa.endereco[id_endereco-1].cidade           = request.POST['endereco[cidade]']
            empresa.endereco[id_endereco-1].numero           = request.POST['endereco[numero]']
            empresa.endereco[id_endereco-1].estado           = request.POST['endereco[estado]']
            empresa.endereco[id_endereco-1].CEP              = request.POST['endereco[CEP]']
            empresa.endereco[id_endereco-1].tipo_logradouro  = request.POST['endereco[tipoLogradouro]']
            empresa.endereco[id_endereco-1].tipo             = request.POST['endereco[tipo]']
            empresa.endereco[id_endereco-1].complemento      = request.POST['endereco[complemento]']
            empresa.endereco[id_endereco-1].bairro           = request.POST['endereco[bairro]']
            empresa.endereco[id_endereco-1].referencia       = request.POST['endereco[referencia]']
            empresa.save()
          else:
            send = Entidade.objects(id=id_entidade).update(push__endereco = params)
          result = {'result': 1, 'params':params, 'id_entidade': id_entidade} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
        except:
          result = {'result': 0} 
          return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
    else:
      result = {'result': 0} 
      return HttpResponse(json.dumps(result, ensure_ascii=False),
              content_type='application/json')
  else:
    template = loader.get_template('app/funcionarios.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarFuncionario(request):
  if 'id' in request.GET:
    funcionarios = Entidade.objects(id=request.GET['id'])
  elif not 'filtro' in request.GET:
    funcionarios = Entidade.objects(tipo = 'FUNCIONARIO')
  else:
    filtro = request.GET['filtro']
    funcionarios = Entidade.objects(Q(tipo = 'FUNCIONARIO') & (Q(nome__icontains=filtro) | Q(nome_RG=filtro) | Q(CPF=filtro)))

  data = []
  for row in funcionarios:
    data.append(json.loads(row.to_json()))
  #
  return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def saidas(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method == 'POST':
    if context['saida'] == 1 :  
      id_saida = request.POST['id']
      produtos = json.loads(request.POST['produtos'])
      produtos_array = []
      if id_saida == '0': #novo
        saida = Saida()
        produtos_array = produtos
      else: #editar
        saida = Saida.objects(id=id_saida)[0]
        for j in produtos:
          flag = 0
          for i in saida.produtos:
            if i['produto'] == j['produto']:
              flag = 1
          if flag == 0:
            produtos_array.append(j)           
      #
      saida_cliente       = Entidade.objects(id=request.POST['cliente'])[0]
      saida.cliente       = saida_cliente.nome
      saida.cliente_id    = request.POST['cliente']
      saida_funcionario   = Entidade.objects(id=request.POST['funcionario'])[0]
      saida.funcionario   = saida_funcionario.nome
      saida.funcionario_id= request.POST['funcionario']
      saida.total         = request.POST['total']    
      saida.produtos      = produtos
      
      saida.save(commit = True)
      id_gerado = str(saida.id)
      result = {'result': id_gerado}
      atualizarEstoque('saida', produtos_array, '0')
    else:
      result = {'result': 0}
    return HttpResponse(json.dumps(result, ensure_ascii=False),
          content_type='application/json')
  else:
    template = loader.get_template('app/saidas.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def buscarSaida(request):
  if request.method == 'GET':
    if 'id' in request.GET:
      saida = Saida.objects(id=request.GET['id'])
    elif 'mes' in request.GET:
      mes = datetime.datetime.strptime(request.GET['mes'], "%d/%m/%Y")
      if mes.month < 12:
        data_final = mes.replace(month=mes.month+1)
      else:
        data_final = mes.replace(month=1, year=mes.year+1)
      saida = Saida.objects(Q(data_cadastro__gte=mes) & Q(data_cadastro__lt=data_final))
    elif not 'filtro' in request.GET:
      saida = Saida.objects()
    else:
      filtro = request.GET['filtro']
      saida = Saida.objects(Q(fornecedor__icontains=filtro) | Q(cliente__icontains=filtro))

    data = []
    for row in saida:
      data.append(json.loads(row.to_json()))
    #
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@login_required(login_url='/login/')
def excluirSaida(request):
  permissoes =  request.user.user_permissions[0].id
  context = literal_eval(permissoes)
  if request.method =='POST':
    if context['saida'] == 1:
      saida = Saida.objects(id=request.POST['id'])
      saida.delete()
      result = {'result':1}
    else:
      result = {'result':0}
    return HttpResponse(json.dumps(result, ensure_ascii=False),content_type='application/json')