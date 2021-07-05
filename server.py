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
    status = service.update_types(pokemon_name,types)
    if status:
        s=200
    else:
        s=400
    return Response(status=s)

@app.route("/getByType/<type>",methods=['GET'])
def get_by_type(type):
    pokemon=service.find_by_type(type)
    return Response(json.dumps(pokemon))


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


@app.route('/evolvePokemon', methods=['PUT'])
def evolve_pokemon():
    pokemon_name = request.get_json()['pokemon_name']
    trainer = request.get_json()['trainer']
    url = "https://pokeapi.co/api/v2/pokemon/"+pokemon_name
    pok_species_url = requests.get(url, verify=False).json()['species']['url']
    evolution_chain_url = requests.get(pok_species_url, verify=False).json()['evolution_chain']['url']
    evolves_to_list = requests.get(evolution_chain_url, verify=False).json()['chain']['evolves_to']
    if evolves_to_list == []:
        return
    else:
        evolves_to = evolves_to_list[0]['species']['name']
        if not service.does_pokemon_exist(evolves_to):
            pokemon_url = "https://pokeapi.co/api/v2/pokemon/"+evolves_to
            pokemon_data = requests.get(pokemon_url, verify=False).json()
            id = pokemon_data['id']
            height = pokemon_data['height']
            weight = pokemon_data['weight']
            types = [i["type"]["name"] for i in pokemon_data["types"]]
            service.add_pokemon(id,evolves_to,height,weight,types)
        service.evolve_pokemon(pokemon_name,trainer,evolves_to)

    

    return Response(json.dumps(evolves_to))




if __name__ == '__main__':
    app.run(port=3000)

