"""Import para trabalhar com banco de dados SQLite"""
import sqlite3
import json
from datetime import datetime, timedelta
from flask import request, jsonify
from dynaconf import settings


# Listas de inclusão
listaNovos = []
listaExistentes = []
saidaDados = []


def db_connection():
    """Classe utilizada para abir a conexão com o banco"""
    try:
        conn = sqlite3.connect('usuarios.sqlite')
    except sqlite3.Error as erro_conexao:
        print(erro_conexao)
    return conn


def abre_jason(dados_json):
    """Classe utilizada para abir arquivo JSON (Pode ser trocada por URL)"""
    with open(dados_json, 'r') as myfile:
        data = myfile.read()
    return json.loads(data)


def limpa_listas():
    """Classe utilizada para limpar list utilizadas"""
    listaNovos.clear()
    listaExistentes.clear()
    saidaDados.clear()
    return True


def calcula_data(number_days):
    """Classe utilizada para calcular o inicio da data de pesquisa"""
    return datetime.today().date() - timedelta(days=(int(number_days)))


def configure(app):
    """Classe Principal do APP"""
    @app.route('/')
    def home():
        return "WORC"

    @app.route('/candidates', methods=['GET'])  # Alfi
    def candidates():
        # Pega dados a serem cadastrados
        json_data = abre_jason(settings.arquivoNovos)
        # Limpa listas
        limpa_listas()
        # Abrindo conexão com o banco
        connection = db_connection()
        cursor = connection.cursor()
        for i in json_data:
            # Valores capturados para domada de decisão
            cnpj = i["document"]
            nome_cliente = i["name"]
            sobre_cliente = i["sobrenome"]
            tipo_doc = i["type_document"]
            job = i["job"]
            cont_tipo = i["contacts"]["type"]
            tel = i["contacts"]["number"]
            data_cad = str(datetime.today())
            data_atual = None

            try:
                cursor.execute(settings.sqlInsert, (cnpj, nome_cliente,
                                                    sobre_cliente, tipo_doc,
                                                    job, cont_tipo, tel,
                                                    data_cad, data_atual))
                connection.commit()
                listaNovos.append(cnpj)
            except:
                connection.rollback()
                listaExistentes.append(cnpj)
        # Fechando conexão
        connection.close()
        # Retorno dos dados
        saidaDados.append({'TotalNovos': len(listaNovos),
                           'Inseridos:': listaNovos,
                           'TotalExiste': len(listaExistentes),
                           'Existentes:': listaExistentes})

        return json.dumps(saidaDados)

    @app.route('/candidates/1', methods=['GET'])
    def candidates1():
        # Pega dados a serem cadastrados
        json_data = abre_jason(settings.arquivosAlterados)
        # Limpa listas
        limpa_listas()

        # Abrindo conexão com o banco
        connection = db_connection()
        cursor = connection.cursor()

        for i in json_data:
            # Valores capturados para domada de decisão
            cnpj = i["document"]
            nome_cliente = i["name"]
            sobre_cliente = i["sobrenome"]
            cont_tipo = i["contacts"]["type"]
            tel = i["contacts"]["number"]
            data_atual = str(datetime.today())

            try:
                cursor.execute(settings.sqlUpdate, (nome_cliente,
                               sobre_cliente, cont_tipo, tel, data_atual, cnpj))
                connection.commit()
                listaExistentes.append(cnpj)
            except:
                connection.rollback()
                listaNovos.append(cnpj)
        # Fechando conexão
        connection.close()
        # Retorno dos dados
        saidaDados.append({'TotalAtualizados': len(listaExistentes),
                           'Atualizados:': listaExistentes})

        return json.dumps(saidaDados)

    @app.route('/contacts', methods=['GET'])
    def contacts():
        number_days = request.args.get('numberDays')
        # Limpando Listas
        limpa_listas()

        # Abrindo conexão com o banco
        connection = db_connection()
        cursor = connection.cursor()

        if number_days is not None:
            # Devolvendo usuarios de um determinado periodo
            cursor.execute(settings.sqlCadPeriodo, (calcula_data(number_days),
                                                    (datetime.today().date()),
                                                    ))
            linha = cursor.fetchall()

            for users in linha:
                listaExistentes.append(users)

            if listaExistentes is not None:
                return jsonify(listaExistentes)
            else:
                return "400"
        else:
            # Devolvendo usuarios do dia
            cursor.execute(settings.sqlCadastros,
                           ((datetime.today().date()),
                            (datetime.today().date()),))
            linha = cursor.fetchall()
            for users in linha:
                listaExistentes.append(users)

            if listaExistentes is not None:
                return jsonify(listaExistentes)
            else:
                return "400"

    @app.route('/contacts/1', methods=['GET'])
    def contacts1():
        number_days = request.args.get('numberDays')
        # Limpando Listas
        limpa_listas()
        # Abrindo conexão com o banco
        connection = db_connection()
        cursor = connection.cursor()
        if number_days is not None:
            # Devolvendo usuarios de um determinado periodo
            cursor.execute(settings.sqlAtuPeriodo, (calcula_data(number_days),
                                                    (datetime.today().date()),
                                                    ))
            linha = cursor.fetchall()
            for users in linha:
                listaExistentes.append(users)

                if listaExistentes is not None:
                    return jsonify(listaExistentes)
                else:
                    return "400"
        else:
            # Devolvendo usuarios do dia
            cursor.execute(settings.sqlAtualizacao,
                           ((datetime.today().date()),
                            (datetime.today().date()),))
            linha = cursor.fetchall()
            for users in linha:
                listaExistentes.append(users)

            if listaExistentes is not None:
                return jsonify(listaExistentes)
            else:
                return "400"
