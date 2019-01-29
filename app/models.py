from __future__ import unicode_literals

from django.db import models

from django_mongoengine import Document,DynamicDocument,EmbeddedDocument, fields, DynamicEmbeddedDocument
from mongoengine import GenericReferenceField, ReferenceField as MongoReferenceField
from django_mongoengine.mongo_auth.models import User
import datetime
import bson

# Create your models here.
class Contato(EmbeddedDocument):
	tipo     = fields.StringField(max_length = 10,blank = True)
	DDD      = fields.StringField(max_length = 3,blank = True)
	telefone = fields.StringField(max_length = 15,blank = True)
	nome     = fields.StringField(max_length = 200, blank = True)
	email    = fields.StringField(max_length = 100,blank = True) 

class Endereco(EmbeddedDocument):
	ESTADO_CHOICES = (
		(u'',u''),
		(u'AC',u'AC'),
		(u'AL',u'AL'),
		(u'AP',u'AP'),
		(u'AM',u'AM'),
		(u'BA',u'BA'),
		(u'CE',u'CE'),
		(u'DF',u'DF'),
		(u'ES',u'ES'),
		(u'GO',u'GO'),
		(u'MA',u'MA'),
		(u'MT',u'MT'),
		(u'MS',u'MS'),
		(u'MG',u'MG'),
		(u'PA',u'PA'),
		(u'PB',u'PB'),
		(u'PR',u'PR'),
		(u'PE',u'PE'),
		(u'PI',u'PI'),
		(u'RJ',u'RJ'),
		(u'RN',u'RN'),
		(u'RS',u'RS'),
		(u'RO',u'RO'),
		(u'RE',u'RR'),
		(u'SC',u'SC'),
		(u'SP',u'SP'),
		(u'SE',u'SE'),
		(u'TO',u'TO'),
	)
	tipo            = fields.StringField(max_length = 20,blank = True)
	CEP	            = fields.StringField(max_length = 15,blank = True)
	tipo_logradouro = fields.StringField(max_length=20,blank = True)
	logradouro      = fields.StringField(max_length = 100,blank = True)
	numero          = fields.StringField(max_length = 10,blank = True)
	bairro          = fields.StringField(max_length = 100,blank = True)
	complemento     = fields.StringField(max_length = 100,blank = True)
	referencia      = fields.StringField(max_length = 100,blank = True)
	cidade          = fields.StringField(max_length = 100,blank = True)
	estado          = fields.StringField(max_length = 2, choices = ESTADO_CHOICES, default = 'SP',blank = True)

class Fornecedor(EmbeddedDocument):
	produtos = fields.DynamicField(blank = True)

class Marca(Document):
	nome = fields.StringField(max_length=200,blank = True)

class HistoricoProduto(Document):
	_id           = fields.StringField(max_length=200,blank = True)
	nome          = fields.StringField(max_length=200,blank = True)
	marca         = fields.StringField(max_length=200,blank = True)
	data_cadastro = fields.DateTimeField(default = datetime.datetime.now())
	preco         = fields.StringField(max_length = 18,blank = True)
	fornecedor    = fields.DynamicField(blank = True)

class Produto(EmbeddedDocument):
	_id            = fields.StringField(max_length=200,blank = True)
	produto_nome   = fields.StringField(max_length=200,blank = True)
	codigo         = fields.StringField(max_length=200,blank = True)
	unidade        = fields.StringField(max_length = 18,blank = True)
	data_cadastro  = fields.DateTimeField(default = datetime.datetime.now())
	estoque_minimo = fields.StringField(max_length = 18,blank = True)
	estoque_atual  = fields.StringField(max_length = 18,blank = True)
	fornecedor     = fields.DynamicField(blank = True)
	preco          = fields.StringField(max_length = 18,blank = True)
	marca          = fields.StringField(max_length = 18,blank = True)

class Funcionario(EmbeddedDocument):
	_id            = fields.StringField(max_length=200,blank = True)
	cargo          = fields.StringField(max_length=200,blank = True)
	salario         = fields.StringField(max_length=200,blank = True)

class Cliente(EmbeddedDocument):
	descricao = fields.StringField(max_length=20, default ='CLIENTE')

class EntidadeAbstract(DynamicDocument):
	produtos              = fields.ListField(blank = True)
	ativo                 = fields.BooleanField(default=False,blank = True)
	endereco              = fields.ListField(fields.EmbeddedDocumentField(Endereco), blank = True)
	contato               = fields.ListField(fields.EmbeddedDocumentField(Contato), blank = True)
	observacao            = fields.StringField(max_length = 400,blank = True)
	nome                  = fields.StringField(max_length=200,blank = True)
#class PJ(Entidade):
	CNPJ                  = fields.StringField(max_length = 19,blank = True)
	nome_fantasia         = fields.StringField(max_length = 100,blank = True)
	inscricao_estadual    = fields.StringField(max_length = 18,blank = True)
	inscricao_municipal   = fields.StringField(max_length = 18,blank = True)
	data_fundacao         = fields.DateTimeField(blank = True)
	CRT                   = fields.StringField(max_length = 18,blank = True)
#class PF(Entidade):
	CPF                   = fields.StringField(max_length = 18,blank = True)
	RG                    = fields.StringField(max_length = 18,blank = True)	
	registro              = fields.StringField(max_length = 18,blank = True)
	data_nascimento       = fields.DateTimeField(blank = True)
	sexo                  = fields.StringField(max_length = 18,blank = True)
	estado_civil          = fields.StringField(max_length = 18,blank = True)
	nome_pai              = fields.StringField(max_length = 50,blank = True)
	nome_mae              = fields.StringField(max_length = 50,blank = True)
	nome_conjuge          = fields.StringField(max_length = 50,blank = True)
	grau_instrucao        = fields.StringField(max_length = 18,blank = True)
	complemento_instrucao = fields.StringField(max_length = 18,blank = True)
	instituicao_ensino    = fields.StringField(max_length = 18,blank = True)
	RA                    = fields.StringField(max_length = 18,blank = True)
	ano_letivo            = fields.StringField(max_length = 18,blank = True)
	periodo               = fields.StringField(max_length = 18,blank = True)
	meta                  = {'abstract': True}

class Entidade(EntidadeAbstract):
	data_cadastro = fields.DateTimeField(default = datetime.datetime.now())
	tipo_pessoa   = fields.StringField(max_length = 40, blank = True) # PF OU PJ
	tipo          = fields.StringField(max_length=20)
	detalhes      = fields.DynamicField(blank = True)
	def save(self, *args, **kwargs):
		if self.tipo == 'PRODUTO':
			marca = Marca.objects(nome=self.detalhes.marca)
			if not marca:
				marca = Marca()
				marca.nome = self.detalhes.marca
				marca.save()
			historico               = HistoricoProduto()
			historico.nome          = self.nome
			historico.marca         = self.detalhes.marca
			historico.data_cadastro = datetime.datetime.now()
			historico.fornecedor    = self.detalhes.fornecedor
			historico.save()
		super(Entidade, self).save(*args, **kwargs)

class Compra(Document):
	data_cadastro = fields.DateTimeField(default = datetime.datetime.now())
	fornecedor_id = fields.StringField(max_length=200,blank = True)
	fornecedor    = fields.StringField(max_length=200,blank = True)
	total         = fields.StringField(max_length=200,blank = True)
	produtos      = fields.DynamicField()

class Saida(Document):
	data_cadastro = fields.DateTimeField(default = datetime.datetime.now())
	fornecedor_id = fields.StringField(max_length=200,blank = True)
	fornecedor    = fields.StringField(max_length=200,blank = True)
	cliente_id    = fields.StringField(max_length=200,blank = True)
	cliente       = fields.StringField(max_length=200,blank = True)
	total         = fields.StringField(max_length=200,blank = True)
	produtos      = fields.DynamicField()
				
class GrupoAcesso(DynamicDocument):
	descricao = fields.StringField(max_length=200)
	acessos   = fields.DynamicField()
	def save(self, *args, **kwargs):
		super(GrupoAcesso, self).save(*args, **kwargs)

class Usuario(EntidadeAbstract):
	usuario      = fields.StringField(max_length=40)
	senha        = fields.StringField(max_length=200)
	nome         = fields.StringField(max_length=200)
	user_permissions  = fields.StringField(max_length=200)
	grupo_acesso = fields.ReferenceField(GrupoAcesso,blank = True)
	userid       = fields.DynamicField()
	email        = fields.StringField(max_length = 200)
	imagem       = fields.DynamicField(blank=True)

	def save(self, *args, **kwargs):
		self.usuario = self.usuario.upper()
		if not self.userid:
			self.cadastro = datetime.datetime.now()
			try:	
				temp = User.create_user(self.usuario,self.senha,self.email)
				temp.update(user_permissions = bson.dbref.DBRef('permissions', [self.user_permissions]))
			except:
				return
			self.userid = str(temp.id)
		else:
			temp = User.objects.get(id = self.userid)
			temp.set_password(self.senha)
			temp.save()
			temp.update(user_permissions = bson.dbref.DBRef('permissions', [self.user_permissions]))
		#
		self.senha = temp.password
		#
		super(Usuario, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.userid:
			user = User.objects.get(id = self.userid)
			user.delete()

		super(Usuario, self).delete(*args,**kwargs)