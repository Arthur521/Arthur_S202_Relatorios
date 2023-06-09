class Post:

    #um objeto post possui todos esses dados:
    def __init__(self, db, texto, textface, nome):
        self.texto = texto
        self.textface = textface
        self.nome = nome
        self.db = db

    #aqui o objeto eh exibido
    def exibir_post(self):
        print()
        print("-" * 40)
        print(f"      {self.nome}")
        print(f"{self.textface} {self.texto}")
        print("-" * 40)

    #e aqui o no eh criado
    def create(self):
        query = """
        MATCH (u:User {nome: $nome})
        CREATE (u)-[:Postou]->(p:Post {nome: $nome, textface: $textface, texto: $texto})
        """
        parameters = {
            "nome": self.nome,
            "textface": self.textface,
            "texto": self.texto,
        }
        self.db.execute_query(query, parameters)
