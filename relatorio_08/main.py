from database import Database
from game_database import GameDatabase

db = Database("bolt://54.205.63.235:7687", "neo4j", "navies-surpluses-pace")
db.drop_all()

game_db = GameDatabase(db)

#Criando jogadores
game_db.create_player("Jao123")
game_db.create_player("Mary4")
game_db.create_player("Zels7")

#Cria a partida, o nome do ganhador e sua pontuacao
game_db.create_match("Partida1", "Jao123", 10)
game_db.create_match("Partida2", "Mary4", 10)
game_db.create_match("Partida3", "Zels7", 10)

#Atualiza o player
game_db.update_player("Jao123", "John123")

#Apaga o player
game_db.delete_player("John123")

#Registra um player em partida junto com a sua pontuacao
game_db.insert_player_match("Mary4", "Partida1", 9)
game_db.insert_player_match("Zels7", "Partida2", 8)
game_db.insert_player_match("Zels7", "Partida1", 7)

#Apaga Partida
game_db.delete_match("Partida3")

#Mostrar dados da Partida1
print("Jogadores e suas pontuacoes na Partida 2:")
print(game_db.get_match_players("Partida2"))
print("Vencedor partida 2:")
print(game_db.get_match_winner("Partida2"))

#Mostrar histórico de partidas de um player
print("Historico de partidas de Zels7:")
print(game_db.get_player_matches("Zels7"))

#Mostra todos jogadores e todas as partidas que participaram
print("Todos players:")
print(game_db.get_player())
print("Todas partidas:")
print(game_db.get_match())

db.close()