from corrida import Corrida
from passageiro import Passageiro
from motorista import Motorista

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


class MotoristaCLI(SimpleCLI):
    def __init__(self, motorista_model):
        super().__init__()
        self.motorista_model = motorista_model
        self.add_command("criar", self.create_motorista)
        self.add_command("procurar", self.read_motorista)
        self.add_command("atualizar", self.update_motorista)
        self.add_command("deletar", self.delete_motorista)

    def create_motorista(self):
        id = input("Motorista ID: ")
        nota = input("Entre com a nota do motorista: ")
        nCorridas = int(input("Quantas corridas o motorista fez? "))
        corridaList = []
        for i in range(0, nCorridas):
            corridaId = input("Corrida ID: ")
            nota = input("Corrida nota: ")
            distancia = input("Corrida distancia: ")
            valor = input("Corrida valor: ")

            print("Agora preencha os dados do passageiro:")
            passageiroId = input("ID do passageiro: ")
            passageiroNome = input("Nome do passageiro: ")
            passageiroDocumento = input("Documento do passageiro: ")

            passageiro = Passageiro(passageiroId, passageiroNome, passageiroDocumento)
            corrida = Corrida(corridaId, nota, distancia, valor, passageiro)
            corridaList.append(corrida)
        motorista = Motorista(id, nota, corridaList)
        self.motorista_model.create_motorista(motorista)

    def read_motorista(self):
        id = input("Entre com o id: ")
        motorista = self.motorista_model.read_motorista_by_id(id)
        if motorista:
            print(f"Nota do motorista: {motorista['nota']}")
            for i in range(len(motorista['corridas'])):
                print(f"Corrida ID: {motorista['corridas'][i].id}:")
                print(f"Nota: {motorista['corridas'][i].nota}")
                print(f"Distancia: {motorista['corridas'][i].distancia}")
                print(f"Valor: {motorista['corridas'][i].valor}")
                print(f"Caregiver Name: {motorista['corridas'][i].passageiro.nome}")
                print(f"Caregiver Document: {motorista['corridas'][i].passageiro.documento}")

    def update_motorista(self):
        id = input("Motorista ID: ")
        nota = input("Entre com a nota do motorista: ")
        nCorridas = int(input("Quantas corridas o motorista fez? "))
        corridaList = []
        for i in range(0, nCorridas):
            corridaId = input("Corrida ID: ")
            nota = input("Corrida nota: ")
            distancia = input("Corrida distancia: ")
            valor = input("Corrida valor: ")

            print("Agora preencha os dados do passageiro:")
            passageiroId = input("ID do passageiro: ")
            passageiroNome = input("Nome do passageiro: ")
            passageiroDocumento = input("Documento do passageiro: ")

            passageiro = Passageiro(passageiroId, passageiroNome, passageiroDocumento)
            corrida = Corrida(corridaId, nota, distancia, valor, passageiro)
            corridaList.append(corrida)
        motorista = Motorista(id, nota, corridaList)
        
        self.motorista_model.update_motorista(motorista)

    def delete_motorista(self):
        id = input("Entre com o id: ")
        self.motorista_model.delete_motorista(id)
        
    def run(self):
        print("Bem-vindo ao cli de motoristas!")
        print("Comandos disponiveis: criar, procurar, atualizar, deletar, sair")
        super().run()
        
