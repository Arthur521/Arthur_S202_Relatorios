from database import Banco
from sistemaGeral import userCLI

#conexao do bd
db = Banco("bolt://44.201.18.99:7687", "neo4j", "fracture-wartime-hand")

#roda sistema
CLI = userCLI(db)
CLI.run()

#fecha o bd
db.close()