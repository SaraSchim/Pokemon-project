from server import get_by_type
import service
import requests

def test_get_pokemon_by_id():
    assert "eevee" in service.find_by_type("normal")
    url="http://127.0.0.1:3000/updateType/eevee"
    assert requests.put(url=url,verify=False).status_code==400
    


def test_add_pokemon():
    bug_url = 'http://localhost:3000/getByType/bug'
    bug_res = requests.get(url=bug_url)
    flying_url = 'http://localhost:3000/getByType/flying'
    flying_res = requests.get(url=flying_url)
    assert 'yanma' in bug_res.json()
    assert 'yanma' in flying_res.json()

def test_update_types():
    poison_url = 'http://localhost:3000/getByType/poison'
    poison_res = requests.get(url=poison_url)
    grass_url = 'http://localhost:3000/getByType/grass'
    grass_res = requests.get(url=grass_url)
    assert 'venusaur' in poison_res.json()
    assert 'venusaur' in grass_res.json()

def test_get_pokmones_by_owner():
    pokemons_url = 'http://localhost:3000/pokemonByTrainer/drasna'
    pokemon_res=requests.get(url = pokemons_url)
    assert pokemon_res.json()==["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe", "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]

def test_get_owners_by_pokemon():
    owners_url = 'http://localhost:3000/trainerByPokemon/charmander'
    owners_res=requests.get(url = owners_url)
    assert owners_res.json()==["Giovanni", "Jasmine", "Whitney"]

def test_evolve():
    evolve_url = 'http://localhost:3000/evolvePokemon'
    pinsir_res = requests.put(url = evolve_url,json={"pokemon_name":"pinsir","trainer":"whitney"})
    assert pinsir_res.status_code==400
    arcie_res = requests.put(url = evolve_url,json={"pokemon_name":"spearow","trainer":"archie"})
    assert arcie_res.status_code==400
    # oddish_res = requests.put(url = evolve_url,json={"pokemon_name":"oddish","trainer":"whitney"})
    # assert oddish_res.status_code==200
    oddish_res = requests.put(url = evolve_url,json={"pokemon_name":"oddish","trainer":"whitney"})
    assert oddish_res.status_code==400
    owners_url = 'http://localhost:3000/pokemonByTrainer/whitney'
    owners_res=requests.get(url = owners_url)
    assert "gloom" in owners_res.json()
    assert "pikachu" in owners_res.json()
    assert "raichu" in owners_res.json()
    pikachu_res = requests.put(url = evolve_url,json={"pokemon_name":"pikachu","trainer":"whitney"})
    assert pikachu_res.status_code==200


