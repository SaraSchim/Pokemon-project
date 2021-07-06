import requests


def get_pokemon_data(pokemon_name):
    url = "https://pokeapi.co/api/v2/pokemon/"+pokemon_name
    res = requests.get(url, verify=False)
    return res



def get_pokemon_data_2(url):
    res = requests.get(url, verify=False)
    return res

