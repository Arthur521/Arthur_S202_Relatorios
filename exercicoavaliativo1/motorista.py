from corrida import Corrida
from typing import List

class Motorista():
    def __init__(self, id: str, nota: int, corridas: List[Corrida]):
        self.id = id
        self.nota = nota
        self.corridas = corridas