from database import Database
from writeAJson import writeAJson
from bookModel import BookModel
from cli import PersonCLI

db = Database(database="relatorio_05", collection="pessoas")
bookModel = BookModel(database=db)


personCLI = PersonCLI(bookModel)
personCLI.run()
