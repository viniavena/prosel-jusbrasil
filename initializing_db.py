# arquivo para inicializar o db com os valores padroes dos tribunais

# import sqlite3

# conn = sqlite3.connect('tribunais.db')

# cursor = conn.cursor()

# cursor.execute('''CREATE TABLE IF NOT EXISTS tribunais (
#                     tribunal_id TEXT PRIMARY KEY,
#                     uf TEXT,
#                     base_url TEXT
#                   )''')

# tribunais = {
#     '02': {'uf': 'AL', 'base_url': 'https://www2.tjal.jus.br'},
#     '06': {'uf': 'CE', 'base_url': 'https://esaj.tjce.jus.br'}
# }

# for codigo, dados in tribunais.items():
#     uf = dados['uf']
#     base_url = dados['base_url']
#     cursor.execute("INSERT INTO tribunais (tribunal_id, uf, base_url) VALUES (?, ?, ?)",
#                    (codigo, uf, base_url))

# conn.commit()
# conn.close()
