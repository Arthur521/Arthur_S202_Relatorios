from database import Database
from writeAJson import writeAJson
from productAnalyzer import ProductAnalyzer

db = Database(database="mercado", collection="compras")
db.resetDatabase()

analisador = ProductAnalyzer(db)

analisador.totalDeVendas(db)
analisador.produtoMaisVendido(db)
analisador.clienteMaisGastador(db)
analisador.listarProdutos(db)