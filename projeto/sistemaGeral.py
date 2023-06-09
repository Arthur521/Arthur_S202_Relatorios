from usuario import Usuario
from post import Post

class SimpleCLI:
    def __init__(self):
        self.commands = {}
        self.logado = False

    #funcao add command ve o nome do comando e roda ele(que eh outra funcao)
    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            #mensagem de comandos dependendo se o usuario esta logado ou nao
            if self.logado == False:
                print()
                print("-" * 40)
                print("Escreva: 'entrar' para logar em sua conta, 'criar' para criar conta, ou 'sair'")
                print("-" * 40)
            if self.logado == True:
                print()
                print("-" * 40)
                print("Escreva: 'procurar' para encontrar uma pessoa, 'ver' para ver sua própria conta, 'postar' para postar algo,")
                print("'atualizar' para atualizar seus dados, 'apagar' para apagar sua conta ou 'sair' para sair do aplicativo")
                print("-" * 40)
            print()
            print("-" * 40)
            #entrada do comando
            command = input("Comando: ")
            print("-" * 40)

            #o comando pode fechar o aplicativo, ou eh usado, ou esta errado
            if command == "sair":
                print()
                print("-" * 40)
                print("Tchau tchau!")
                print("-" * 40)
                break
            elif command in self.commands:
                print()
                print("-" * 40)
                self.commands[command]()
                print("-" * 40)
            else:
                print()
                print("-" * 40)
                print("Comando errado, tente denovo!")
                print("-" * 40)


class userCLI(SimpleCLI):

    #define o bd, os comandos e suas respectivas funcoes
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.add_command("entrar", self.entrar_user)
        self.add_command("criar", self.create_user)
        self.add_command("procurar", self.procurar_user)
        self.add_command("ver", self.ver_user)
        self.add_command("postar", self.postar_user)
        self.add_command("atualizar", self.update_user)
        self.add_command("apagar", self.delete_user)
        
    #funcao que cria o usuario como objeto e chama o método desse objeto que cria o nó
    def create_user(self):
        if self.logado == False:
            email = input("Entre com o email do usuário: ")
            senha = input("Entre com a senha do usuário: ")
            nome = input("Entre com o nome do usuário: ")
            idade = input("Entre com a idade do usuário: ")
            textface = input("Entre com o seis letras para o perfil: ")
            status = input("Entre com seu status: ")
            print("-" * 40)
            self.usuario = Usuario(self.db, nome, idade, email, senha, 3, status, textface)
            self.usuario.create()
            self.logado = True
        else:
            print("Você já está logado!!!")
            print("-" * 40)
    
    #usuario pode ver seu proprio perfil
    def ver_user(self):
        self.usuario.read(self.usuario.nome)

    #acessa sua conta
    def entrar_user(self):
        email = input("Entre com o email do usuário: ")
        senha = input("Entre com a senha do usuário: ")
        print("-" * 40)

        #coleta os dados do perfil
        query = "MATCH (t:User {email: $email, senha: $senha}) RETURN t.nome as nome, t.idade as idade, t.nota as nota, t.status as status, t.textface as textface"
        parameters = {"email": email, "senha": senha}
        results = self.db.execute_query(query, parameters)

        if not results:
            print()
            print("-" * 40)
            print("Email ou senha incorretos.")
            return
        
        usuarios = []
        for result in results:
            self.logado = True
            nome = result["nome"]
            idade = result["idade"]
            nota = result["nota"]
            status = result["status"]
            textface = result["textface"]
            usuario = Usuario(self.db, nome, idade, email, senha, nota, status, textface)
            usuarios.append((idade, email, nota))
            print()
            print("-" * 40)
            print("Você entrou!")
    
        self.usuario = usuario
        return usuarios
    
    #o usuario pode criar o objeto de seu post aqui
    def postar_user(self):
        texto = input("Digite seu post: ")
        postagem = Post(self.db, texto, self.usuario.textface, self.usuario.nome)

        #e aqui ele vai usar o método do objeto para criar o nó do post
        postagem.create()

    #aqui ele vai procurar o perfil de um usuario especifico pelo nome
    def procurar_user(self):

        #introduz o nome que esta bucando
        nome = input("Entre com o nome do usuário: ")
        print("-" * 40)
        print()
        print("-" * 40)

        #se a nota nao for maior que 0, significa que o usuario nao existe, consequentemente,
        #ele nao vai ser lido
        nota = self.usuario.read(nome) #metodo do objeto usuario que busca outros usuarios 
        if nota > 0:
            print()
            print("-" * 40)

            #e aqui o usuario eh avaliado 
            nota_dada = input("Avalie esse usuário: ")

            #o metodo vai levar os dados do usuario que esta avaliando junto com o que esta sendo avaliado
            #esses dados servem para criar uma relacao entre os usuarios e claro, atualizar a nota do avaliado
            self.usuario.avalia(self.usuario.nome, nome, self.usuario.nota, nota_dada, nota)

    #atualiza os dados do usuario
    def update_user(self):
        #uma confirmacao, como o padrao de muitos aplicativos
        email_atual = input("Entre com o seu email atual: ")
        senha_atual = input("Entre com a sua senha atual: ")
        print("-" * 40)
        print()
        print("-" * 40)
        
        #atualiza os dados do usuario
        email = input("Entre com a novo email: ")
        senha = input("Entre com a nova senha: ")
        nome = input("Entre com o novo nome: ")
        self.usuario.nome = nome
        idade = input("Entre com a idade atual: ")
        textface = input("Entre com o seis letras para o perfil: ")
        status = input("Entre com o novo status: ")

        #usa o metodo do objeto usuario para atualizar os dados
        self.usuario.update(email_atual, senha_atual, email, senha, nome, idade, textface, status)

    #deleta o usuario, faz confimarcao e executa o metodo do objeto usuario
    def delete_user(self):
        email = input("Entre com o seu email: ")
        senha = input("Entre com a sua senha: ")
        self.usuario.delete(email, senha)
    
    #metodo que inicia o aplicativo
    def run(self):
        print()
        print()
        print()
        print("-" * 40)
        print("Seja bem-vindo ao NOSEDIVE! Avalie seus amigos e seus posts com notas de 1 a 5!")
        print("-" * 40)
        super().run()