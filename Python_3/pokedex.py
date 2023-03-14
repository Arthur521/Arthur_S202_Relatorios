from typing import Collection
import pymongo # pip install pymongo
from dataset.pokemon_dataset import dataset


class Database:
    def __init__(self, database, collection):
        self.connect(database, collection)

    def connect(self, database, collection):
        try:
            connectionString = "localhost:27017"
            self.clusterConnection = pymongo.MongoClient(
                connectionString,
                tlsAllowInvalidCertificates=True
            )
            self.db = self.clusterConnection[database]
            self.collection = self.db[collection]
            print("Conectado ao banco de dados com sucesso!")
        except Exception as e:
            print(e)

    def resetDatabase(self):
        try: 
            self.db.drop_collection(self.collection)
            self.collection.insert_many(dataset)
            print("Banco de dados resetado com sucesso!")
        except Exception as e:
            print(e)
 
    
    def mostrarTodos(self):
        return self.collection.find()

    def buscarPelaFraqueza(self, type: str):
        return self.collection.find({"weaknesses": type})
    
    def buscarPeloDoce(self, doce: str):
        return self.collection.find({"candy": doce})

    def buscarPeloTipo(self, type: str):
        return self.collection.find({"type": type})

    def buscarPeloNumero(self, id: int):
        return self.collection.find({"id": id})



