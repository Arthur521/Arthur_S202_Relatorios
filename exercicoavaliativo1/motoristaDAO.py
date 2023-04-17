from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List
from corrida import Corrida
from motorista import Motorista
from passageiro import Passageiro

class MotoristaDAO:
    def __init__(self, database):
        self.db = database

    def create_motorista(self, motorista: Motorista):
        try:
            print(type(motorista.corridas))
            print(type(motorista.corridas[0]))

            for i in range(len(motorista.corridas)):
                motorista.corridas[i] = motorista.corridas[i].toDict()

            res = self.db.collection.insert_one({"_id": motorista.id, "nota": motorista.nota, "corridas" : motorista.corridas})
        except Exception as error:
            print(f"An error occurred while creating this motorista: {error}")

    def read_motorista_by_id(self, motorista_id: str):
        try:
            motorista = self.db.collection.find_one({"id": motorista_id})
            if motorista:
                print(f"Motorista achado: {motorista}")

                corridaList = []
                for i in range(len(motorista["corrida"])):
                    passageiroDict = motorista["corrida"][i]["passageiro"]
                    passageiro = Passageiro(passageiroDict["id"], passageiroDict["nome"], passageiroDict["documento"])
                    corridaDict = motorista["corrida"][i]
                    corrida = Corrida(corridaDict["id"], corridaDict["nota"], corridaDict["distancia"], corridaDict["valor"], passageiro)
                    corridaList.append(corrida)

                motorista = Motorista(motorista["id"], motorista["nome"], motorista["especie"], motorista["idade"], corridaList)
                return motorista
            else:
                print(f"No motorista found with id {motorista_id}")
                return None
        except Exception as error:
            print(f"An error occurred while searching this motorista: {error}")
            return None

    def update_motorista(self, motorista: Motorista):
        try:
            print(type(motorista.corridas))
            print(type(motorista.corridas[0]))

            for i in range(len(motorista.corridas)):
                motorista.corridas[i] = motorista.corridas[i].toDict()

            res = self.db.collection.update_one({"_id": motorista.id, "nota": motorista.nota, "corridas" : motorista.corridas})
        except Exception as error:
            print(f"An error occurred while creating this motorista: {error}")
            return None

    def delete_motorista(self, id: str):
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"motorista deleted: {res.deleted_count} document(s) deleted")
            return res.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting motorista: {e}")
            return None