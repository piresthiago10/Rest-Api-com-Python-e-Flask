from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3

# valores padrões para o filtro
def normalize_path_params(cidade = None, estrelas_min = 0, estrelas_max = 5, diaria_min = 0, diaria_max = 10000, limit = 50, offset = 0, **dados):

    # se cidade estiver preenchida
    if cidade is not None:
        return{
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    # se a cidade não estiver preenchida
    return{
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}

# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type = str)
path_params.add_argument('estrelas_min', type = float)
path_params.add_argument('estrelas_max', type = float)
path_params.add_argument('diaria_min', type = float)
path_params.add_argument('diaria_max', type = float)
path_params.add_argument('limit', type = float) # quantidades de itens para exibir por página
path_params.add_argument('offset', type = float) #quantidade de elementos pulados

class Hoteis(Resource):

    def get(self):

        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        # {'limit': 50, 'diaria_min': None}
        # o dicionário só recebera dados válidos
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        # retorna um dicionarios com os valores normalizados
        parametros = normalize_path_params(**dados_validos)

        # para evitar erros no código é recomendavel utilizar get() ao invés de acessa o valor do dicionário diretamente

        if not parametros.get('cidade'):
            # pega os valores chaves
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4],
            'site_id': linha[5]
            })

        return{'hoteis': hoteis}

        #select * from hoteis
        #return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type = int, required = True, help = "Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
       
        if hotel is not None:
            return hotel.json()
        return {'mesage': 'Hotel not found.'}, 404
        
    @jwt_required #esse decorador exige que o usuario esteja logado para poder executar a função
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' alread exists.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site id.'}, 400

        try:
            hotel.save_hotel()
        except:
            # 500, internal server error
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel() 
            return hotel_encontrado.json(), 200  
        
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            # 500, internal server error
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 
        return hotel.json(), 201 #created

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404




