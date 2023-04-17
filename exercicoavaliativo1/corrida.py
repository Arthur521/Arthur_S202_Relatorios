from passageiro import Passageiro

class Corrida():
    def __init__(self, id: str, nota: int, distancia: float, valor: float, passageiro: Passageiro):
        self.id = id
        self.nota = nota 
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro
    def toDict(self):
        return {"id": self.id, "nota": self.nota, "distancia": self.distancia, "valor": self.valor, "passageiro": self.passageiro.toDict()}