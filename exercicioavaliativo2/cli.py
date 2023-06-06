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


class TeacherCLI(SimpleCLI):
    def __init__(self, teacher_crud):
        super().__init__()
        self.teacher_crud = teacher_crud
        self.add_command("criar", self.create_teacher)
        self.add_command("procurar", self.read_teacher)
        self.add_command("atualizar", self.update_teacher)
        self.add_command("deletar", self.delete_teacher)

    def create_teacher(self):
        name = input("Entre com o nome do professor: ")
        ano_nasc = int(input("Entre com o ano de nascimento do professor: "))
        cpf = input("Entre com o cpf do professor: ")
        self.teacher_crud.create(name, ano_nasc, cpf)

    def read_teacher(self):
        name = input("Entre com o nome do professor: ")
        teacher = self.teacher_crud.read(name)
        if teacher:
            print("Ano de nascimento e CPF do professor:", teacher)

    def update_teacher(self):
        name = input("Entre com o novo nome: ")
        ano_nasc = int(input("Entre com o 'novo' ano de nascimento: "))
        cpf = input("Entre com o 'novo' cpf: ")
        self.teacher_crud.update(name, ano_nasc, cpf)

    def delete_teacher(self):
        name = input("Entre com o nome: ")
        self.teacher_crud.delete(name)
        
    def run(self):
        print("Bem-vindo ao cli de professores!")
        print("Comandos disponiveis: criar, procurar, atualizar, deletar, sair")
        super().run()