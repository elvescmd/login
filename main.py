from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)
CORS(app)

db_host = '51.79.55.118'
db_user = 'u27_FqWSepCMN2'
db_password = 'HSO.EbAFWQjF!w1JPg1+v!yE'
db_name = 's27_db2'

connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    cursorclass=DictCursor
)

cursor = connection.cursor()

# Cache para armazenar os dados do banco de dados
cached_users = []

def update_cache():
    cursor.execute('SELECT * FROM UserAutenticator')
    global cached_users
    cached_users = cursor.fetchall()

# Atualiza o cache ao iniciar o aplicativo
update_cache()

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    try:
        print('Tentativa de autenticação:', request.json)
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            print('Dados de autenticação ausentes na solicitação.')
            return jsonify({'message': 'Dados de autenticação ausentes.'}), 400

        # Verifica no cache
        user = next((u for u in cached_users if u['Username'] == username), None)

        # Se não encontrado no cache, atualiza o cache a partir do banco de dados
        if not user:
            update_cache()
            user = next((u for u in cached_users if u['Username'] == username), None)

        if user and user['Password'] == password:
            print('Autenticação bem-sucedida!')
            return jsonify({'isLogged': True})

        print('Falha na autenticação.')
        return jsonify({'isLogged': False})

    except Exception as e:
        print('Erro ao autenticar usuário:', str(e))
        return jsonify({'message': 'Erro interno do servidor.'}), 500

if __name__ == '__main__':
    app.run(port=3000)
