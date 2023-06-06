class TeacherCRUD:
    def __init__(self, database):
        self.db = database

    def create(self, name, ano_nasc, cpf):
        query = "CREATE (t:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})"
        parameters = {"name": name, "ano_nasc": ano_nasc, "cpf": cpf}
        self.db.execute_query(query, parameters)

    def read(self, name):
        query = "MATCH (t:Teacher {name: $name}) RETURN t.ano_nasc as ano_nasc, t.cpf as cpf"
        parameters = {"name": name}
        results = self.db.execute_query(query, parameters)
        return [(result["ano_nasc"], result["cpf"])  for result in results]

    def delete(self, name):
        query = "MATCH (t:Teacher {name: $name}) DELETE t"
        parameters = {"name": name}
        self.db.execute_query(query, parameters)

    def update(self, name, new_cpf):
        query = "MATCH (t:Teacher {name: $name}) SET t.cpf = $new_cpf"
        parameters = {"name": name, "new_cpf": new_cpf}
        self.db.execute_query(query, parameters)