from dynaconf import settings             
from flask import request, jsonify, redirect
import sqlite3
from datetime import datetime, timedelta
import json


#Listas de inclusão
listaNovos = []
listaExistentes = []
saidaDados = []

def db_connection():
   conn = None
   try:
      conn = sqlite3.connect('usuarios.sqlite')
   except sqlite3.Error as e:
      print(e)
   return conn

def abreJson(dadosJson):
   with open(dadosJson, 'r') as myfile:
      data=myfile.read()
   return json.loads(data)

def limpaListas():
   listaNovos.clear()
   listaExistentes.clear()
   saidaDados.clear()
   return True


def configure(app):
   
   @app.route('/')
   def home():
      return  "WORC" 

   @app.route('/candidates', methods=['GET'])  #Alfi
   def candidates():
      # Pega dados a serem cadastrados
      jsonData = abreJson(settings.arquivoNovos)

      #Limpa listas
      limpaListas()

      # Abrindo conexão com o banco
      connection = db_connection()
      cursor     = connection.cursor() 

      for i in jsonData:
         #Valores capturados para domada de decisão
         CNPJ = i["document"]
         nomeCliente = i["name"]
         sobrNomeeCliente = i["sobrenome"]
         tipoDocumento = i["type_document"]
         job = i["job"]
         contatoTipo = i["contacts"]["type"]
         telefone = i["contacts"]["number"]
         dataCadastro = str(datetime.today())
         dataAtualizacao = None

         try:
            cursor.execute(settings.sqlInsert,(CNPJ,nomeCliente,sobrNomeeCliente,tipoDocumento,job,contatoTipo,telefone,dataCadastro,dataAtualizacao)) 
            connection.commit()
            listaNovos.append(CNPJ)
         except:
            connection.rollback()
            listaExistentes.append(CNPJ)

      # Fechando conexão
      connection.close()
      # Retorno dos dados
      saidaDados.append({'TotalNovos': len(listaNovos), 'Inseridos:': listaNovos, 'TotalExiste': len(listaExistentes), 'Existentes:': listaExistentes })
      return json.dumps(saidaDados)

   
   @app.route('/candidates/1', methods=['GET'])
   def candidates1():
      # Pega dados a serem cadastrados
      jsonData = abreJson(settings.arquivosAlterados)
      #Limpa listas
      limpaListas()

      # Abrindo conexão com o banco
      connection = db_connection()
      cursor     = connection.cursor() 

      for i in jsonData:
         #Valores capturados para domada de decisão
         CNPJ = i["document"]
         nomeCliente = i["name"]
         sobNomeCliente = i["sobrenome"]
         contatoTipo = i["contacts"]["type"]
         telefone = i["contacts"]["number"]
         dataAtualizacao = str(datetime.today())

         try:
            cursor.execute(settings.sqlUpdate,(nomeCliente,sobNomeCliente,contatoTipo,telefone,dataAtualizacao,CNPJ,)) 
            connection.commit()
            listaExistentes.append(CNPJ)
         except:
            connection.rollback()
            listaNovos.append(CNPJ)

      # Fechando conexão
      connection.close()
      # Retorno dos dados
      saidaDados.append({'TotalAtualizados': len(listaExistentes), 'Atualizados:': listaExistentes })
      return json.dumps(saidaDados)
      
      

   @app.route('/contacts', methods=['GET'])
   def contacts():
      numberDays = request.args.get('numberDays')

      # Limpando Listas
      limpaListas() 
     
      # Abrindo conexão com o banco
      connection = db_connection()
      cursor     = connection.cursor() 

      if numberDays != None:
         # Devolvendo usuarios de um determinado periodo
         cursor.execute(settings.sqlCadPeriodo,((datetime.today().date() - timedelta(days= (int(numberDays)))),(datetime.today().date()),))
         linha = cursor.fetchall()
         for users in linha:
            listaExistentes.append(users)
         
         if listaExistentes is not None:
            return jsonify(listaExistentes)
         else:
            return ("400")
      else:
         # Devolvendo usuarios do dia
         cursor.execute(settings.sqlCadastros,((datetime.today().date()),(datetime.today().date()),))
         linha = cursor.fetchall()
         for users in linha:
            listaExistentes.append(users)
         
         if listaExistentes is not None:
            return jsonify(listaExistentes)
         else:
            return ("400")
         
   @app.route('/contacts/1', methods=['GET'])
   def contacts1():
      numberDays = request.args.get('numberDays')

      # Limpando Listas
      limpaListas() 
     
      # Abrindo conexão com o banco
      connection = db_connection()
      cursor     = connection.cursor() 

      if numberDays != None:
         # Devolvendo usuarios de um determinado periodo
         cursor.execute(settings.sqlAtuPeriodo,((datetime.today().date() - timedelta(days= (int(numberDays)))),(datetime.today().date()),))
         linha = cursor.fetchall()
         for users in linha:
            listaExistentes.append(users)
         
         if listaExistentes is not None:
            return jsonify(listaExistentes)
         else:
            return ("400")
      else:
         # Devolvendo usuarios do dia
         cursor.execute(settings.sqlAtualizacao,((datetime.today().date()),(datetime.today().date()),))
         linha = cursor.fetchall()
         for users in linha:
            listaExistentes.append(users)
         
         if listaExistentes is not None:
            return jsonify(listaExistentes)
         else:
            return ("400")