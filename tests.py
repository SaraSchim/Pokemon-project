from server import get_by_type
import service
import requests

def test_get_pokemon_by_id():
    assert "eevee" in service.find_by_type("normal")
    url="http://127.0.0.1:3000/updateType/eevee"
    assert requests.put(url=url,verify=False).status_code==400
    

def test_add_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon/yanma"
    pokemon_data = requests.get(url, verify=False).json()
    id = pokemon_data['id']
    height = pokemon_data['height']
    weight = pokemon_data['weight']
    types = [i["type"]["name"] for i in pokemon_data["types"]] 
    service.add_pokemon(id,"yanma",height,weight,types)
test_add_pokemon()
# def test_add_pokemon():
#     bug_url = 'http://localhost:3000/getByType/bug'
#     bug_res = requests.get(url=bug_url)
#     flying_url = 'http://localhost:3000/getByType/flying'
#     flying_res = requests.get(url=flying_url)
#     assert bug_res == [{'name': 'yanma'}] 
#     assert flying_res == [{'name': 'yanma'}]
# test_add_pokemon()

# def evolve():
#     evolve_url="http://127.0.0.1:3000/evolvePokemon/"
#     res = requests.get(url=evolve_url)
#     print(res)

