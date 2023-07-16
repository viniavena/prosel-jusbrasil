#
# Arquivo contendo as funções de busca no banco de dados de tribunais
#

import sqlite3

path_database = 'tribunais.db'

# Classe tribunal
class Tribunal:
    def __init__(self, tribunal_id, uf, base_url):
        self.tribunal_id = tribunal_id
        self.uf = uf
        self.base_url = base_url



# Funcoes
def listar_tribunais():
    '''
    Função para listar todos os tribunais da tabela homônima

    Output:
    ------
    tribunais: lista de objetos da classe Tribunal contendo as informações dos tribunais.
    '''

    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tribunais")
    resultados = cursor.fetchall()

    tribunais = []
    for resultado in resultados:
        tribunal = Tribunal(tribunal_id=resultado[0], 
                            uf=resultado[1], 
                            base_url=resultado[2])
        
        tribunais.append(tribunal)

    conn.close()
    
    return tribunais
