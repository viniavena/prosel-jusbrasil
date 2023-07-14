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
    