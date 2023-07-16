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


def buscar_tribunal_por_id(tribunal_id):
    '''
    Função para buscar um tribunal pelo seu ID.

    Parâmetros:
    ----------
    tribunal_id: str
        ID do tribunal a ser buscado.

    Output:
    ------
    tribunal: objeto Tribunal contendo as informações do tribunal encontrado, ou None se não encontrado.
    '''

    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tribunais WHERE tribunal_id = ?", (tribunal_id,))
    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        tribunal = Tribunal(tribunal_id=resultado[0], 
                            uf=resultado[1], 
                            base_url=resultado[2])
        return tribunal
    else:
        return None


def adiciona_tribunal(tribunal: Tribunal):
    '''
    Função para adicionar um tribunal à tabela de tribunais.

    Parâmetros:
    ----------
    tribunal: objeto Tribunal contendo as informações do tribunal a ser adicionado à tabela

    '''
    
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO tribunais (tribunal_id, uf, base_url) VALUES (?, ?, ?)", 
                    (tribunal.tribunal_id, 
                    tribunal.uf, 
                    tribunal.base_url))
        conn.commit()
        conn.close()
        return True
    
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return False
