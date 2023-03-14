from pokedex import Database
from helper.writeAJson import writeAJson

pokedex = Database(database = "pokedex", collection = "pokemons")

#pokedex.resetDatabase()


writeAJson(pokedex.mostrarTodos(), "todosPokemon")
writeAJson(pokedex.buscarPelaFraqueza("Grass"), "buscarPelaFraqueza")
writeAJson(pokedex.buscarPeloTipo("Fire"), "buscandoPeloTipo")
writeAJson(pokedex.buscarPeloDoce("Bulbasaur Candy"), "buscarPeloDoce")
writeAJson(pokedex.buscarPeloNumero(1), "buscarPeloNumero")
