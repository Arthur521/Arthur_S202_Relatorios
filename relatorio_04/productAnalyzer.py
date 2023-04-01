from writeAJson import writeAJson

class ProductAnalyzer:
    def __init__(self, database):
        self.mediaDeGasto(database)
        self.melhorCliente(database)

    def mediaDeGasto(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$cliente_id", "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$group": {"_id": None, "media": {"$avg": "$total"}}}
        ])
        writeAJson(result, "Média de gasto total")

    def melhorCliente(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": {"cliente": "$cliente_id", "data": "$data_compra"}, "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"_id.data": 1, "total": -1}},
            {"$group": {"_id": "$_id.data", "cliente": {"$first": "$_id.cliente"}, "total": {"$first": "$total"}}}
        ])
        writeAJson(result, "Cliente que mais comprou em cada dia")
    
    def totalDeVendas(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": {"data": "$data_compra"}, "total": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"_id.data": 1}},
            {"$group": {"_id": "$_id.data", "total": {"$first": "$total"}}}
        ])
        writeAJson(result, "Total de compras")

    def produtoMaisVendido(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "total": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Produto mais vendido")

    def clienteMaisGastador(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": {"cliente": "$cliente_id", "data": "$data_compra"}, "total": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$group": {"_id": "$_id.cliente", "total": {"$sum": "$total"}}}, 
            {"$sort": {"total": -1}},
            {"$limit": 1}
        ])
        writeAJson(result, "Cliente que mais comprou")
    
    def listarProdutos(self, database):
        result = database.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao"}},
            {"$sort": {"total": -1}},
        ])
        writeAJson(result, "Produtos")