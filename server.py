from client import get_pokemon_data, get_pokemon_data_2
from flask import Flask, Response, request
import json
import service


app = Flask(__name__)

# run 'GET' with url 'http://127.0.0.1:3000/trainerByPokemon/...'
# in the ... put the pokemon name you want to get his trainers
@app.route("/trainerByPokemon/<pokemon_name>", methods=['GET'])
def get_trainer_by_pokemon(pokemon_name):
    res = service.find_owners(pokemon_name)
    if res=="pokemon doesn't exist":
        return Response(res,status=404)
    if res=="DB Error":
        return Response(res,status=501)
    return Response(json.dumps(res),status=200)


# run 'GET' with url 'http://127.0.0.1:3000/pokemonByTrainer/...'
# in the ... put the trainer name who you want to get his pokemons
@app.route('/pokemonByTrainer/<trainer_name>', methods=['GET'])
def get_pokemon_by_trainer(trainer_name):
    res = service.find_roster(trainer_name)
    if res=="trainer doesn't exist":
        return Response(res,status=404)
    if res=="DB Error":
        return Response(res,status=501)
    return Response(json.dumps(res),status=200)



# run 'PUT' with url 'http://127.0.0.1:3000/updateType/...'
# in the ... put the pokemon name you want to update his types
@app.route("/updateType/<pokemon_name>",methods=['PUT'])
def update_pokemon_type(pokemon_name):
    res = get_pokemon_data(pokemon_name)
    if res.status_code==404:
        return Response("pokemon doesn't exist",status=404)
    types=[i["type"]["name"] for i in res.json()["types"]]
    status = service.update_types(pokemon_name,types)
    if status:
        return Response("updated {}'s types".format(pokemon_name),status=200)
    else:
        return Response("DB Error",status=501)



# run 'GET' with url 'http://127.0.0.1:3000/getByType/...'
# in the ... put the type which you want to get the pokemons who have this type
@app.route("/getByType/<type>",methods=['GET'])
def get_by_type(type):
    res=service.find_by_type(type)
    if res=="type does not exist":
        return Response(res,status=404)
    if res=="DB Error":
        return Response(res,status=501)
    return Response(json.dumps(res),status=200)


# run 'POST' with url 'http://127.0.0.1:3000/addPokemon'
# in the body put a json object: {"id": ..., "name": ..., "height": ..., "weight": ..., "types": ...} with the new pokemon's details
@app.route('/addPokemon', methods=['POST'])
def add_pokemon():
    data = request.get_json()
    if not (data.get('id') and data.get('name') and data.get('height') and data.get('weight') and data.get('types')):
        return Response("missing some required arguments",status=400)
    res = service.add_pokemon(data['id'], data['name'],data['height'],data['weight'],data['types'])
    if res:
        return Response(res,501)
    return Response("pokemon {} added".format(data['name']))



# run 'DELETE' with url 'http://127.0.0.1:3000/deletePokemon/...'
# in the ... put the pokemon name you want to delete
@app.route('/deletePokemon/<pokemon_name>', methods=['DELETE'])
def delete_pokemon(pokemon_name):
    res = service.delete_pokemon(pokemon_name)
    if res=="pokemon doesn't exist":
        return Response(res, 404)
    if res=="DB Error":
        return Response(res, 501)
    return Response("pokemon {} deleted".format(pokemon_name))



# run 'PUT' with url 'http://127.0.0.1:3000/evolvePokemon'
# in the body put a json object: {"pokemon_name": ..., "trainer": ...} with the pokemon of the trainer which you evolve
@app.route('/evolvePokemon', methods=['PUT'])
def evolve_pokemon():
    pokemon_name = request.get_json()['pokemon_name']
    trainer = request.get_json()['trainer']
    pok_species_url = get_pokemon_data(pokemon_name)
    if pok_species_url.status_code==404:
        return Response("pokemon doesn't exist",status=404)
    evolution_chain_url = get_pokemon_data_2(pok_species_url.json()['species']['url']).json()['evolution_chain']['url']
    evolves_to_list = get_pokemon_data_2(evolution_chain_url).json()['chain']['evolves_to']
    if evolves_to_list == []:
        return Response("pokemon cannot evolve",status=400)
    else:
        evolves_to = evolves_to_list[0]['species']['name']
        if not service.does_pokemon_exist(evolves_to):
            pokemon_data = get_pokemon_data(evolves_to).json()
            id = pokemon_data['id']
            height = pokemon_data['height']
            weight = pokemon_data['weight']
            types = [i["type"]["name"] for i in pokemon_data["types"]]
            service.add_pokemon(id,evolves_to,height,weight,types)
        res = service.evolve_pokemon(pokemon_name,trainer,evolves_to)
        if res=="trainer doesn't exist" or res== "the owner does not have this pokemon":
            return Response(res,status=404)
        if res=="evolved pokemon already exists":
            return Response(res,status=500)    
        if res=="DB Error":
            return Response(res,status=501)
    return Response(json.dumps(evolves_to),status=200)





