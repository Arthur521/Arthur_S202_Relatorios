from post import Post

class Usuario:
    #usuario quando criado recebe todos esses dados:
    def __init__(self, db, nome, idade, email, senha, nota, status, textface):
        self.db = db
        self.nome = nome
        self.idade = idade
        self.email = email
        self.senha = senha
        self.nota = nota
        self.status = status
        self.textface = textface

    #o metodo create transforma o objeto Usuario em um nó "User"
    def create(self):
        query = "CREATE (t:User {nome: $nome, idade: $idade, email: $email, senha: $senha, nota: $nota, status: $status, textface: $textface})"
        parameters = {"nome": self.nome, "idade": self.idade, "email": self.email, "senha": self.senha, "nota": self.nota, "status": self.status, "textface": self.textface}
        self.db.execute_query(query, parameters)
        
    #o metodo read serve para mostrar a página do usuario identificado por "nome"
    def read(self, nome):

        #aqui vamos coletar esses dados diretamente do bd
        query = """
        MATCH (u:User {nome: $nome})
        RETURN u.idade as idade, u.nota as nota, u.status as status, u.textface as textface
        """
        parameters = {"nome": nome}
        results = self.db.execute_query(query, parameters)
        if not results:
            print("Nome incorreto.")
            return 0
        for result in results:
            status = result["status"]
            textface = result["textface"]
            idade = result["idade"]
            nota = result["nota"]

        #e aqui vamos mostra-los para o usuario que esta usando o programa
        print("")
        print(f"  {textface}")
        print("")
        print(f"  {nome}, nota: {nota}")
        print(f"    Idade: " + str(idade))
        print(f"    " + str(status))
        print("")
        print("-" * 40)

        #em seguida, serão coletados os dados dos posts do usuario buscado
        query_posts = """
        MATCH (u:User {nome: $nome})-[:Postou]->(p:Post)
        RETURN p.textface as textface, p.texto as texto, p.nome as nome, p.timestamp as timestamp
        ORDER BY p.timestamp DESC
        LIMIT 10
        """
        parameters_posts = {"nome": nome}
        results_posts = self.db.execute_query(query_posts, parameters_posts)

        for result_post in results_posts:
            nome_post = result_post["nome"]
            textface_post = result_post["textface"]
            texto_post = result_post["texto"]

            #aqui o objeto post é criado
            post = Post(self.db, texto_post, textface_post, nome_post)

            #e em seguida, exibido
            post.exibir_post()

        #o usuario buscado nao tem posts
        if not results_posts:
            print()
            print("-" * 40)
            print("Sem posts")
            print("-" * 40)

        return nota
    
    #metodo para apagar o usuario
    def delete(self, email, senha):
        query = "MATCH (u:User {email: $email, senha: $senha}) DETACH DELETE u"
        parameters = {"email": email, "senha": senha}
        self.db.execute_query(query, parameters)

    #metodo para atualizar informações do usuario
    def update(self, email_atual, senha_atual, email, senha, nome, idade, textface, status):
        query = "MATCH (t:User {email: $email_atual, senha: $senha_atual}) SET t.email = $email, t.senha = $senha, t.nome = $nome, t.idade = $idade, t.textface = $textface, t.status = $status"
        parameters = {"email_atual": email_atual, "senha_atual": senha_atual, "email": email, "senha": senha, "nome": nome, "idade": idade, "textface": textface, "status": status}
        self.db.execute_query(query, parameters)
    
    #aqui um usuario avalia outro
    def avalia(self, nome_avaliador, nome, nota_avaliador, nota_dada, nota):

        #o calculo da nota dada, usa de peso a nota do avaliador,
        #em seguida, é somada com a nota do avaliado
        #se tornando a nota final do avaliado
        nota_dada = float(nota_dada)
        if nota_dada > 2:
            nota += nota_dada * float(nota_avaliador) * 0.01
        else:
            nota -= nota_dada * float(nota_avaliador) * 0.01
        nota = round(nota, 3) #arredondamento de 3 casas
        
        #atualiza a nota do avaliado
        query_user = "MATCH (u:User {nome: $nome}) SET u.nota = $new_nota"
        parameters_user = {"nome": nome, "new_nota": nota}
        self.db.execute_query(query_user, parameters_user)

        #cria (ou atualiza) uma relação que armazena a nota que um usuario deu para outro
        query_rel = """
        MATCH (u1:User {nome: $nome_avaliador}), (u2:User {nome: $nome})
        MERGE (u1)-[r:Avaliou]->(u2)
        SET r.nota = $nota_dada
        """
        parameters_rel = {"nome_avaliador": nome_avaliador, "nome": nome, "nota_dada": nota_dada}
        self.db.execute_query(query_rel, parameters_rel)