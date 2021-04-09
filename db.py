import sqlite3

conn = sqlite3.connect("usuarios.sqlite")

cursor = conn.cursor()

sql_query = """CREATE TABLE "usuario" (
	"CNPJ"	TEXT NOT NULL UNIQUE,
	"Nome"	TEXT NOT NULL,
	"sobrenome"	TEXT NOT NULL,
	"tipoDocumento"	TEXT NOT NULL,
	"job"	TEXT NOT NULL,
	"contatoTipo"	TEXT NOT NULL,
	"contatoNumero"	TEXT NOT NULL,
	"dataCadastro" TIMESTAMP,
	"dataAtualizacao" TIMESTAMP,
	PRIMARY KEY("CNPJ")
)"""

cursor.execute(sql_query)