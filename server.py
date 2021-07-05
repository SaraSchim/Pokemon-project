from flask import Flask, Response, request
import json
import service
import requests
app = Flask(__name__)

@app.route("/trainerByPokemon/<pokemon_name>", methods=['GET'])
def pokemon_by_trainer(pokemon_name):
    res = service.find_owners(pokemon_name)
    return Response(json.dumps(res))

@app.route("/updateType/<pokemon_name>",methods=['PUT'])
def update_pokemon_type(pokemon_name):
    url = "https://pokeapi.co/api/v2/pokemon/"+pokemon_name
    res = requests.get(url, verify=False).json()
    types=[i["type"]["name"] for i in res["types"]]
    service.update_types(pokemon_name,types)
    return ''

@app.route("/getByType/<type>",methods=['GET'])
def get_by_type(type):
    pokemon=service.find_by_type(type)
    return Response(json.dumps(pokemon))

@app.route("/evolve/<pokemon_name>",methods=['PUT'])
def evolve(pokemon_name):
    url = "https://pokeapi.co/api/v2/pokemon/"+pokemon_name
    pokemon_info=requests.get(url, verify=False).json()
    species_url = pokemon_info["species"]["url"]
    species_info = requests.get(species_url, verify=False).json()
    chain_url=species_info.get("evolution_chain")
    chain_info=requests.get(chain_url, verify=False).json()
    
    return ''

if __name__ == '__main__':
    app.run(port=3000)
import json
import service
from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/pokemonByTrainer/<trainer_name>', methods=['GET'])
def get_pokemon_by_trainer(trainer_name):
    res = service.find_roster(trainer_name)
    return Response(json.dumps(res))



@app.route('/addPokemon', methods=['POST'])
def add_pokemon():
    data = request.get_json()
    res = service.add_pokemon(data['id'], data['name'],data['height'],data['weight'],data['types'])
    return Response("added")


@app.route('/deletePokemon/<pokemon_name>', methods=['DELETE'])
def delete_pokemon(pokemon_name):
    res = service.delete_pokemon(pokemon_name)
    return Response("deleted")



if __name__ == '__main__':
    app.run(port=3000)

