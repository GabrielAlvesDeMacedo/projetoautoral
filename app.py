from flask import Flask, request, render_template
import requests

app = Flask(__name__)

traducao = {
    'normal': 'Normal', 
    'dragon': 'Dragão', 
    'psychic': 'Psíquico', 
    'electric': 'Elétrico', 
    'ground': 'Terra', 
    'ice': 'Gelo', 
    'rock': 'Pedra', 
    'dark': 'Noturno', 
    'bug': 'Inseto', 
    'steel': 'Aço', 
    'fire': 'Fogo', 
    'water': 'Água', 
    'grass': 'Planta', 
    'fighting': 'Lutador', 
    'poison': 'Veneno', 
    'fairy': 'Fada', 
    'ghost': 'Fantasma', 
    'flying': 'Voador'
}

API_ENDPOINT = 'https://pokeapi.co/api/v2/pokemon/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        numero = int(request.form['numero'])

        if not numero or numero < 0 or numero > 1025:
            return render_template('index.html', erro='Número não permitido')
        
        pokemon = numero

        response = requests.get(API_ENDPOINT + str(pokemon))

        if response.status_code == 200:
            data = response.json()
            nome = data["name"].capitalize()
            tipos = [traducao.get(tipo["type"]["name"], tipo["type"]["name"]) for tipo in data["types"]]
            imagem = data["sprites"]["front_default"]
            altura = data["height"] * 10
            peso = data["weight"] / 10
            habilidade = [ability["ability"]["name"] for ability in data["abilities"]]

            
            return render_template('index.html', numero=numero, nome=nome, imagem=imagem, tipos=tipos, height=altura, weight=peso, abilities=habilidade,)
        else:
            return render_template('index.html', erro='Erro no sistema! Esse pokemon não existe!')
    return render_template('index.html')

@app.route('/detalhespoke/<int:numero>')
def detalhespoke(numero):
    response = requests.get(API_ENDPOINT + str(numero))
    if response.status_code == 200:
        data = response.json()
        nome = data["name"].capitalize()
        tipos = [traducao.get(tipo["type"]["name"], tipo["type"]["name"]) for tipo in data["types"]]
        imagem = data["sprites"]["front_default"]
        altura = data["height"] * 10
        peso = data["weight"] / 10
        habilidade = [ability["ability"]["name"] for ability in data["abilities"]]
        return render_template('detalhespoke.html', numero=numero, nome=nome, imagem=imagem, tipos=tipos, altura=altura, peso=peso, habilidade=habilidade)
    else:
        return render_template('detalhespoke.html', erro='Erro no sistema! Esse pokemon não existe!')


if __name__ == '__main__':
    app.run(debug=True)