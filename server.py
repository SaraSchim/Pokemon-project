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

