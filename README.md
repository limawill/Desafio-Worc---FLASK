# Desafio_Worc_FLASK
## Desafio Startup WORC

Este projeto é executado no micro framework Python: Flask.

## Dependencias

- Flask==1.1.2
- dynaconf==3.1.4
- DateTime==4.3

## Como rodar localmente
O Software foi desenvolvido no linux  Fedora 32, o app será executado dentro e um container Docker 

### Docker

Com o docker instalado na maquina rodar os seguintes comandos:
```sh
docker build -t flask:latest .
```
Após a compilação:
```sh
docker run -d -p 5000:5000 flask
```
Caso não tenha nenhum problema rodando o comando:
```sh
docker ps -a
```
Terá uma saida semelhante a está
```sh
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS         PORTS                    NAMES
292e3f98c6f4   flask     "flask run"   4 seconds ago   Up 2 seconds   0.0.0.0:5000->5000/tcp   gifted_brahmagupta
```
E no seu navegador de preferencia acessar:
```sh
http://127.0.0.1:5000/
```

## Como rodar os testes
Após o flask estar ativo acesse:
```sh
http://127.0.0.1:5000
```
### URL /candidates
```sh
http://127.0.0.1:5000/candidates
```
Esta URL é responde a solicitação do **Alfi** a de inclusão de novos usuarios, é verificado pelo CNPJ se o cadastro já existe caso não o mesmo inclui, se já existir é informado no retorno que o usuario já existe. Para simulação os dados do usuario vem do arquivo: **dadosCadastros.json**

### URL /candidates/1
```sh
http://127.0.0.1:5000/candidates/1
```
Esta URL é responde a solicitação do **Samuca** a de realizar o update dos usuarios que estão na base de dados, atualizando somente os campos:
- Nome
- Sobrenome
- Tipo do contato
- Telefone

A realização da atualização é realizado pela verificação do CNPJ na base. O retorno infoma quantos usuarios foram atualizados com sucesso cadastro. Para simulação os dados do usuario vem do arquivo: **dadosAlterados.json**


### URL /contacts
```sh
http://127.0.0.1:5000/contacts
```
Esta URL é responde a uma das solicitações do **Fabricio** a de verificação dos novos canditados (usuarios), automaticamente ele retorna no formato **json** todos os usuarios cadastrados no dia da pesquisa.
É possivel realizar pesquisa por periodo, basta incluir na URL um endpoint, conforme o exemplo abaixo:

```sh
http://127.0.0.1:5000/contacts?numberDays=4
```
No exemplo acima a busca será realizada da data atual há 4 dias atrás (Ex: do dia 05/04 até 09/05)


### URL /contacts/1

```sh
http://127.0.0.1:5000/contacts/1
```
Esta URL é responde a uma das solicitações do **Fabricio** a de verificação da atualização dos dados dos usuarios, automaticamente ele retorna no formato **json** todos os usuarios cadastrados no dia da pesquisa.
É possivel realizar pesquisa por periodo, basta incluir na URL um endpoint, conforme o exemplo abaixo:

```sh
http://127.0.0.1:5000/contacts/1?numberDays=4
```
No exemplo acima a busca será realizada da data atual há 4 dias atrás (Ex: do dia 05/04 até 09/05)

## Respostas as solicitações




## Estrutura do projeto
```sh
.
├── README.md                                      
├── Dockerfile
├── Project
|     |── app.py
|     └── views.py
├── settings.toml
├── requirements.txt
└── db.py

├── dadosCadastros.json
├── dadosAlterados.json
```

