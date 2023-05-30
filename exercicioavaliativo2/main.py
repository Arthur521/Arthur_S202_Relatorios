from database import Database
from school_database import SchoolDatabase

# cria uma instância da classe Database, passando os dados de conexão com o banco de dados Neo4j
db = Database("bolt://44.197.243.20:7687", "neo4j", "sand-bureaus-ideal")

# Criando uma instância da classe SchoolDatabase para interagir com o banco de dados
school_db = SchoolDatabase(db)

# Atualizando o nome de um professor

#print(school_db.get_teacher("Renzo"))


# Fechando a conexão com o banco de dados
db.close()