from bs4 import BeautifulSoup
import requests

resultados = []

# ------------
# Classes:


class ParteDoProcesso:
    def __init__(self, tipo_parte, nome_parte, advogados):
        self.tipo_parte = tipo_parte
        self.nome_parte = nome_parte
        self.advogados = advogados

class MovimentacaoProcesso:
    def __init__(self, data_movimentacao, tramite, descricao):
        self.data_movimentacao = data_movimentacao
        self.tramite = tramite
        self.descricao = descricao

class DadosProcesso:
    def __init__(self, numero_processo, juiz, assunto, classe, area, data_distribuicao, valor_acao, partes, movimentacoes, instancia):
        self.numero_processo = numero_processo
        self.instancia = instancia
        self.juiz = juiz
        self.assunto = assunto
        self.classe = classe
        self.area = area
        self.data_distribuicao = data_distribuicao
        self.valor_acao = valor_acao
        self.partes = partes
        self.movimentacoes = movimentacoes


# ------------
# Funções:


def get_pagina_web(url):
    '''
    Função que faz a requisição web para uma página web dado uma url e faz o parse para um objeto BeautifulSoup.

    Essa função utiliza as bibliotecas Requests e BeautifulSoup.

    Input:
    ------
    url: string url da página a ser feita a requisição

    Output:
    retorna um objeto do tipo BeautifulSoup

    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    return soup



def pega_codigo_segunda_instancia(soup_pagina_segunda_instancia_1):
    '''
    Função de extração do código do processo da request inicial de segunda instancia,
    para enfim poder fazer a request com os dados do processo.add()

    Essa função utiliza a biblioteca BeautifulSoup.

    Input:
    ------
    soup_pagina_segunda_instancia_1: objeto BeautifulSoup da página obtida pela request de rota '/cposg5/search.do?cbPesquisa=NUMPROC&dePesquisa='

    Output:
    -------
    retorna string contendo o código do processo na segunda instancia 
    (caso não haja código, ou seja, não haja processo em segunda instancia retorna-se None)

    '''
    
    # Verifica se existe aquele processo em segunda instância
    if soup_pagina_segunda_instancia_1.find('td', id='mensagemRetorno'):
       return None
    
    codigo_processo = soup_pagina_segunda_instancia_1.find('input', id="processoSelecionado").get('value')
    
    return codigo_processo



def pega_partes_do_processo(soup_pagina_processo):
    '''
    Função que extrai as partes do processo (polos ativos e passivos) e seus respectivos advogados.

    Essa função utiliza a biblioteca BeautifulSoup.

    Input:
    ------
    soup_pagina_processo: objeto BeautifulSoup da página obtido pela request '/cpopg/show.do?processo.numero=' ou '/cposg5/show.do?processo.codigo='
    
    Output:
    -------
    Lista contendo objetos da classe ParteDoProcesso
    '''

    lista_das_partes = []

    partes_do_processo = soup_pagina_processo.find('table', id=['tableTodasPartes','tablePartesPrincipais']).find_all('tr', class_='fundoClaro')
    
    for row in partes_do_processo:
        tipo_parte = row.find('span', class_ = 'mensagemExibindo tipoDeParticipacao').get_text().strip()
        nome_parte = row.find('td', class_ = 'nomeParteEAdvogado').contents[0].strip()
        advogados_rows = row.find_all(lambda tag: tag.name == 'span' and tag.text.startswith('Advogad'))
        advogados = [tag.find_next_sibling(string=True).strip() for tag in advogados_rows]

        parte_do_processo = ParteDoProcesso(tipo_parte, nome_parte, advogados)
        lista_das_partes.append(parte_do_processo)

    return lista_das_partes



def pega_movimentacoes_processo(soup_pagina_processo):
    '''
    Função que extrai as movimentações do processo.
    Informações extraidas: data da movimentação, título do trâmite e descrição da movimentação.
    
    Essa função utiliza a biblioteca BeautifulSoup.

    Input:
    ------
    soup_pagina_processo: objeto BeautifulSoup da página obtido pela request '/cpopg/show.do?processo.numero=' ou '/cposg5/show.do?processo.codigo='

    Output:
    ------
    Retorna uma lista de objetos da classe MovimentacaoProcesso
    '''

    lista_movimentacoes = []
    rows_movimentacoes = soup_pagina_processo.find('tbody', id='tabelaTodasMovimentacoes').find_all('tr')

    for row in rows_movimentacoes:
        data_movimentacao = row.find('td', class_= ['dataMovimentacao', 'dataMovimentacaoProcesso']).get_text().strip()
        tag_tramite = row.find('td', class_ = ['descricaoMovimentacao', 'descricaoMovimentacaoProcesso'])
        
        tramite = descricao = ""
        
        if tag_tramite.find('a', class_='linkMovVincProc'):
            tramite = tag_tramite.find('a', class_='linkMovVincProc').text.strip()
            descricao_span = tag_tramite.find('span')
            descricao_parts = [part.strip() for part in descricao_span if not part.name] # Filtra apenas o texto dentro das tags e ignora as tags.
            descricao = " ".join(descricao_parts)
            
        else:
            tramite_parts = [part.strip() for part in tag_tramite if not part.name] 
            tramite = " ".join(tramite_parts).strip()
            descricao_span = tag_tramite.find('span')
            descricao_parts = [part.strip() for part in descricao_span if not part.name]
            descricao = " ".join(descricao_parts)
        
        movimentacao = MovimentacaoProcesso(data_movimentacao, tramite, descricao)
        lista_movimentacoes.append(movimentacao)

    return lista_movimentacoes
    


def pega_infos_processo(soup_pagina_processo, numero_processo, grau_instancia):
    '''
    Função que extrai as informações do cabeçalho do processo.
    Informações extraidas: número do processo, classe, área, data de distribuição, juiz e valor da ação.
    
    Essa função utiliza a biblioteca BeautifulSoup.

    Input:
    ------
    soup_pagina_processo: objeto BeautifulSoup da página obtido pela request '/cpopg/show.do?processo.numero=' ou '/cposg5/show.do?processo.codigo='

    Output:
    ------
    Retorna objeto da classe ParteDoProcesso

    '''

    num_processo = soup_pagina_processo.find('span', id="numeroProcesso").get_text().strip()

    if numero_processo != num_processo:
        raise Exception("Número do processo não condiz com o encontrado.")       

    
    if grau_instancia == 1:
        juiz = soup_pagina_processo.find('span', id='juizProcesso').contents[0]
        assunto = soup_pagina_processo.find('span', id='assuntoProcesso').contents[0]
        classe = soup_pagina_processo.find('span', id='classeProcesso').contents[0]
        data_distribuicao = soup_pagina_processo.find('div', id='dataHoraDistribuicaoProcesso').contents[0]
        valor_acao = soup_pagina_processo.find('div', id='valorAcaoProcesso').contents[0].replace(' ','')

    else:
        juiz = ''
        assunto = soup_pagina_processo.find('div', id='assuntoProcesso').find('span').text
        classe = soup_pagina_processo.find('div', id='classeProcesso').find('span').text
        data_distribuicao = ''
        valor_acao = soup_pagina_processo.find('div', id='valorAcaoProcesso').find('span').text.replace(' ','')


    area = soup_pagina_processo.find('div', id='areaProcesso').get_text().strip()
    partes = pega_partes_do_processo(soup_pagina_processo)  # Função para obter as partes do processo
    movimentacoes = pega_movimentacoes_processo(soup_pagina_processo)

    dados_processo = DadosProcesso(numero_processo, juiz, assunto, classe, area, data_distribuicao, valor_acao, partes, movimentacoes, grau_instancia)

    return dados_processo
