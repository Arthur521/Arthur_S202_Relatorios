class GameDatabase:
    def __init__(self, database):
        self.db = database

    def create_player(self, name):
        query = "CREATE (:Player {name: $name})"
        parameters = {"name": name}
        self.db.execute_query(query, parameters)

    def create_match(self, name, winner_name, score):
        query = "MATCH (p:Player {name: $player_name}) CREATE (:Match {name: $name})<-[:VENCEU]-(p)"
        parameters = {"name": name, "player_name": winner_name}
        self.db.execute_query(query, parameters)
        query = "MATCH (a:Player {name: $player_name}) MATCH (b:Match {name: $name}) CREATE (a)-[:JOGOU {score: $score}]->(b)"
        parameters = {"name": name, "player_name": winner_name, "score": score}
        self.db.execute_query(query, parameters)

    def get_player(self):
        query = "MATCH (p:Player) RETURN p.name AS name"
        results = self.db.execute_query(query)
        return [result["name"] for result in results]

    def get_match(self):
        query = "MATCH (a:Match)<-[:JOGOU]-(p:Player) RETURN a.name AS name, p.name AS player_name"
        results = self.db.execute_query(query)
        return [(result["name"], result["player_name"]) for result in results]

    def update_player(self, old_name, new_name):
        query = "MATCH (p:Player {name: $old_name}) SET p.name = $new_name"
        parameters = {"old_name": old_name, "new_name": new_name}
        self.db.execute_query(query, parameters)
    
    def insert_player_match(self, player_name, match_name, score):
        query = "MATCH (a:Player {name: $player_name}) MATCH (b:Match {name: $match_name}) CREATE (a)-[:JOGOU {score: $score}]->(b)"
        parameters = {"match_name": match_name, "player_name": player_name, "score": score}
        self.db.execute_query(query, parameters)

    def delete_player(self, name):
        query = "MATCH (p:Player {name: $name}) DETACH DELETE p"
        parameters = {"name": name}
        self.db.execute_query(query, parameters)

    def delete_match(self, name):
        query = "MATCH (a:Match {name: $name})<-[:JOGOU]-(p:Player) DETACH DELETE a"
        parameters = {"name": name}
        self.db.execute_query(query, parameters)

    def get_match_players(self, match_name):
        query = "MATCH (:Match {name: $match_name})<-[j:JOGOU]-(p:Player) RETURN p.name AS name, j.score AS score"
        parameters = {"match_name": match_name}
        results = self.db.execute_query(query, parameters)
        return [(result["name"], result["score"]) for result in results]
    
    def get_match_winner(self, match_name):
        query = "MATCH (m:Match {name: $match_name}) <-[:VENCEU]-(p:Player) RETURN p.name AS name"
        parameters = {"match_name": match_name}
        results = self.db.execute_query(query, parameters)
        return [(result["name"]) for result in results]
    
    def get_player_matches(self, player_name):
        query = "MATCH (:Player {name: $player_name})-[:JOGOU]->(m:Match) RETURN m.name AS name"
        parameters = {"player_name": player_name}
        results = self.db.execute_query(query, parameters)
        return [result["name"] for result in results]