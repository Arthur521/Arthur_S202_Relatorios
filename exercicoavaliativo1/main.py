from database import Database
from motoristaDAO import MotoristaDAO
from motoristaCLI import MotoristaCLI

db = Database(database = "dadosDeMotoristas", collection = "motoristas")
motoristaDAO = MotoristaDAO(database = db)


motoristaCLI = MotoristaCLI(motoristaDAO)
motoristaCLI.run()
