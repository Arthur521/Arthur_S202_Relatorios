class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            command = input("Entre com um comando: ")
            if command == "sair":
                print("Xau!")
                break
            elif command in self.commands:
                self.commands[command]()
            else:
                print("Comando errado, tente denovo!")


class PersonCLI(SimpleCLI):
    def __init__(self, book_model):
        super().__init__()
        self.book_model = book_model
        self.add_command("criar", self.create_book)
        self.add_command("procurar", self.read_book)
        self.add_command("atualizar", self.update_book)
        self.add_command("deletar", self.delete_book)

    def create_book(self):
        titulo = input("Entre com o titulo do livro: ")
        autor = input("Entre com o titulo do autor: ")
        ano = int(input("Entre com o ano de lancamento: "))
        preco = input("Entre com o preco do livro: ")
        self.book_model.create_book(titulo, autor, ano, preco)

    def read_book(self):
        id = input("Entre com o id: ")
        book = self.book_model.read_book_by_id(id)
        if book:
            print(f"Nome do livro: {book['titulo']}")
            print(f"Nome do autor: {book['autor']}")
            print(f"Ano de lancamento: {book['ano']}")
            print(f"Preco do livro: {book['preco']}")

    def update_book(self):
        id = input("Entre com o id: ")
        titulo = input("Entre com o novo titulo do livro: ")
        autor = input("Entre com o novo titulo do autor: ")
        ano = int(input("Entre com o 'novo' ano de lançamento: "))
        preco = input("Entre com o novo preço do livro: ")
        self.book_model.update_book(id, titulo, autor, ano, preco)

    def delete_book(self):
        id = input("Entre com o id: ")
        self.book_model.delete_book(id)
        
    def run(self):
        print("Bem-vindo ao cli de livros!")
        print("Comandos disponiveis: criar, procurar, atualizar, deletar, sair")
        super().run()
        
