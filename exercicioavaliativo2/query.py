class Database:
    def __init__(self, database):
        self.db = database

    def get_cities(self):
        query = "MATCH (c:City) RETURN c.name AS name"
        results = self.db.execute_query(query)
        return [result["name"] for result in results]

    def get_teacher(self, teacher_name):
        query = "MATCH (t:Teacher {name: $teacher_name}) RETURN t.ano_nasc AS ano_nasc, t.cpf AS cpf"
        parameters = {"teacher_name": teacher_name}
        results = self.db.execute_query(query, parameters)
        return [(result["ano_nasc"], result["cpf"]) for result in results]
    
    def get_teacher_fletter(self, letra):
        query = "MATCH (t:Teacher) WHERE t.name STARTS WITH $letter RETURN t.name AS name"
        parameters = {"letter": letra}
        results = self.db.execute_query(query, parameters)
        return [result["name"] for result in results]
    
    def get_school_between_numbers(self, num1, num2):
        query = "MATCH (s:School) WHERE $number1 <= s.number <= $number2 RETURN s.name AS name"
        parameters = {"number1": num1, "number2": num2}
        results = self.db.execute_query(query, parameters)
        return [result["name"] for result in results]
    
    def get_youngest_and_oldest_teacher_years(self):
        query = "MATCH (t:Teacher) RETURN min(t.ano_nasc) AS youngest, max(t.ano_nasc) AS oldest"
        results = self.db.execute_query(query)
        return [(result["youngest"], result["oldest"]) for result in results]
    
    def get_population_average(self):
        query = "MATCH (c:City) RETURN avg(c.population) AS media"
        results = self.db.execute_query(query)
        return [result["media"] for result in results]
    
    def get_find_by_cep_new_name(self, cep_enter):
        query = "MATCH (c:City {cep: $cep_enter}) RETURN REPLACE(c.name, 'a', 'A') AS new_name"
        parameters = {"cep_enter": cep_enter}
        results = self.db.execute_query(query, parameters)
        return [result["new_name"] for result in results]
    
    def get_third_letters(self):
        query = "MATCH (t:Teacher) RETURN substring(t.name, 2, 1) AS third_letter"
        results = self.db.execute_query(query)
        return [result["third_letter"] for result in results]