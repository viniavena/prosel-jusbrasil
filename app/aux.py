
from app.scrap import get_pagina_web, pega_codigo_segunda_instancia, pega_infos_processo, pega_movimentacoes_processo, pega_partes_do_processo


urls_rotas = {
    'instancia_1':'/cpopg/show.do?processo.numero=',
    'instancia_2_1':'/cposg5/search.do?cbPesquisa=NUMPROC&dePesquisa=',
    'instancia_2_2':'/cposg5/show.do?processo.codigo='
    }


def valida_numero_processo(numero_processo):
    '''
    Função para validar o número do processo judicial utilizando o algoritmo Módulo 97, Base 10, ISO 7064

    Input:
    ------
    numero_processo: string

    Output:
    -------
    retorna True se o numero é valido e False se esse é invalido
    
    '''

    numero_processo = numero_processo.replace('.','').replace('-', '')
    numero_processo_sem_dv = numero_processo[:7] + numero_processo[9:]

    try:
        dv = 98 - ((int(numero_processo_sem_dv) * 100) % 97)
    except:
        return False

    return int(numero_processo[7:9]) == dv
    
def busca_primeira_instancia(numero_processo, tribunal):
    '''
    Função com o pipeline de busca de um processo para a primeira instância

    Essa função utiliza as classes e funcoes desenvolvidas no modulo scrap

    Input:
    ------
    numero_processo: string contendo o numero do processo a ser buscado
    tribunal: objeto referente ao tribunal refernte ao processo

    Output:
    -------
    Retorna objeto da classe DadosProcesso

    '''

    grau_instancia = 1
    url_busca = tribunal['base_url'] + urls_rotas['instancia_1'] + numero_processo
    
    soup = get_pagina_web(url_busca)
    
    resultado_primeira_instancia = pega_infos_processo(soup,numero_processo,grau_instancia)
    return resultado_primeira_instancia
    
    
def busca_segunda_instancia(numero_processo, tribunal):
    '''
    Função com o pipeline de busca de um processo para a primeira instância

    Essa função utiliza as classes e funcoes desenvolvidas no modulo scrap

    Input:
    ------
    numero_processo: string contendo o numero do processo a ser buscado
    tribunal: objeto referente ao tribunal refernte ao processo

    Output:
    -------
    Retorna objeto da classe DadosProcesso
    (caso não haja código, ou seja, não haja processo em segunda instancia retorna-se None)

    '''

    grau_instancia = 2
    
    url_busca_1 = tribunal['base_url'] + urls_rotas['instancia_2_1'] + numero_processo
    soup_1 = get_pagina_web(url_busca_1)

    codigo_processo_segunda_instancia = pega_codigo_segunda_instancia(soup_1)
    
    # Não há código de processo, ou seja, não há segunda instância, então não executa a busca
    if codigo_processo_segunda_instancia is None:
        return None
    
    url_busca_2 = tribunal['base_url'] + urls_rotas['instancia_2_2'] + codigo_processo_segunda_instancia
    soup_2 = get_pagina_web(url_busca_2)

    resultado_segunda_intancia = pega_infos_processo(soup_2,numero_processo,grau_instancia)

    return resultado_segunda_intancia
    