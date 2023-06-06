from database import Banco
from query import Database
from teacher_crud import TeacherCRUD
from cli import TeacherCLI

db = Banco("bolt://44.197.243.20:7687", "neo4j", "sand-bureaus-ideal")

school_db = Database(db)

teachers_crud = TeacherCRUD(db)

#EXERCICIO 1

#1. Busque pelo professor `“Teacher”` cujo nome seja **“Renzo”**, retorne o **ano_nasc** e o **CPF**.
print(school_db.get_teacher("Renzo"))

#2. Busque pelos professores `“Teacher”` cujo nome comece com a letra **“M”**, retorne o **name** e o **cpf**.
print(school_db.get_teacher_fletter("M"))

#3. Busque pelos nomes de todas as cidades `“City”` e retorne-os.
print(school_db.get_cities())

#4. Busque pelas escolas `“School”`, onde o number seja maior ou igual a 150 e menor ou igual a 550, 
# retorne o nome da escola, o endereço e o número.
print(school_db.get_school_between_numbers(150, 550))


#EXERCICIO 2

#1. Encontre o ano de nascimento do professor mais jovem e do professor mais velho.
print(school_db.get_youngest_and_oldest_teacher_years())

#2. Encontre a média aritmética para os habitantes de todas as cidades, use a propriedade **“population”**.
print(school_db.get_population_average())

#3. Encontre a cidade cujo **CEP** seja igual a **“37540-000”** e retorne o nome com todas as letras **“a”** substituídas por **“A”** .
print(school_db.get_find_by_cep_new_name('37540-000'))

#4. Para todos os professores, retorne um caractere, iniciando a partir da 3ª letra do nome.
print(school_db.get_third_letters())


## Questão 03

#1. Crie a classe `TeacherCRUD()` que tenha uma relação de **composição** com a classe `Database()`e 
# apresente funções de CRUD na entidade `“Teacher”` do banco de dados, utilizando o `name` para fazer os MATCH’s.
#feito

#2. Utilizando a classe `TeacherCRUD()` crie um `Teacher` com as seguintes características:
#teachers_crud.create("Chris Lima", 1956, "189.052.396-66")

#3. Utilizando a classe `TeacherCRUD()` pesquise o professor com o name de `"Chris Lima"`.
print(teachers_crud.read("Chris Lima"))

#4. Utilizando a classe `TeacherCRUD()` altere o cpf do `“Teacher”` de name `"Chris Lima"` para `"162.052.777-77"`
#teachers_crud.update("Chris Lima", "162.052.777-77")

#5. Crie um **CLI utilizando orientação** a objetos **como visto em aula**.
teachersCLI = TeacherCLI(teachers_crud)
teachersCLI.run()

db.close()