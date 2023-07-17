# Prosel-jusbrasil

#### _Desafio técnico de crawler para JusBrasil_

Desenvolvimento de uma API Crawler que busca dados de um processo em todos os graus dos Tribunais de Justiça de Alagoas (TJAL) e do Ceará (TJCE).

## Escopo

- Criar uma API para receber um JSON contendo o número do processo
- Buscar dados de um processo em todos os graus
- Retornar um JSON com os dados dos processos encontrados em todas as esferas

## Features

- Validação do número de processo
- Identificação do tribunal a partir do número do processo
- Busca e extração dos dados do processo em primeira e segunda instância
- Busca de forma paralela entre as diferentes esferas (concorrência)
- Testes unitários
- Banco de dados com tribunais
- Escalabilidade: possibilidade de adicionar novos tribunais ao crawler
- Versionamento de código

## Stack usada

- Linguagem de programação: Python
- Framework FastAPI para criar a API web
- Banco de dados em SQLite3
- Algumas das bibliotecas usadas:
  - BeautifulSoup: Utilizada para fazer o parsing e extrair informações de páginas HTML.
  - Requests: Utilizada para fazer as requisições HTTP
  - Asyncio: Utilizada para executar tarefas assíncronas de forma paralela.
  - Unittest: Utilizada para escrever testes unitários e comparar com resultados esperados.

**Disclaimer:**
Este projeto utiliza o banco de dados localmente, o que não é considerado uma boa prática em ambientes de produção. Essa abordagem foi adotada apenas para fins de apresentação do desafio técnico.

## Instalação

Este documento fornece instruções para a instalação da API. Siga as etapas abaixo para configurar o ambiente e executar a API em seu sistema.

### Requisitos do Sistema

Certifique-se de que seu sistema atenda aos seguintes requisitos:

- Python 3.9 ou superior instalado
- Acesso à internet para instalar dependências e rodar o crawler

### Clonando o Repositório

Para começar, clone o repositório do projeto em um diretório local. Abra o terminal e execute o seguinte comando:

```bash
git clone https://github.com/viniavena/prosel-jusbrasil.git
```

Isso criará uma cópia do projeto em seu sistema.

### Configurando o Ambiente Virtual

Recomendo o uso de um ambiente virtual para isolar as dependências do projeto. Siga as etapas abaixo para configurar um ambiente virtual:

1. No terminal, navegue até o diretório do projeto e crie um novo ambiente virtual:

```bash
python3 -m venv crawler-venv
```

2. Ative o ambiente virtual:

```bash
source crawler-venv/bin/activate
```

Agora você está dentro do ambiente virtual e pronto para instalar as dependências.

### Instalando as Dependências

A API requer algumas dependências para ser executada corretamente. Para instalá-las, execute o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

Isso instalará todas as dependências necessárias para a API.

### Inicializando o Servidor

Após concluir a configuração, você pode iniciar o servidor da API. No terminal, execute o seguinte comando:

```bash
uvicorn main:app --reload
```

Aguarde a mensagem "Uvicorn running on..." no terminal, indicando que o servidor está em execução.

A API agora está rodando em http://localhost:8000 ou em outro endereço e porta especificados pelo Uvicorn.

### Testando a API

A API está pronta para uso. Você pode enviar solicitações para a API usando ferramentas como o cURL, Insomnia, Postman ou qualquer biblioteca HTTP de sua preferência.

Consulte a seguinte documentação da API para obter mais detalhes sobre os endpoints disponíveis e os formatos das solicitações e respostas.

### Demo

Uma demonstração da API está disponível [aqui](https://proseljusbrasil-1-w8214358.deta.app/).

Você também pode acessar uma documentação interativa da API [aqui](https://proseljusbrasil-1-w8214358.deta.app/redoc).

**Disclaimer:** Na versão publicada na demo, não é utilizado multithreading entre as diferentes esferas e não é possível adicionar ou deletar tribunais da tabela.

### Documentação endpoints API

Uma vez inicializado o servidor é possível acessar uma documentação automática e interativa por meio de: http://127.0.0.1:8000/redoc

A documentação a seguir descreve os endpoints disponíveis na API.

#### Bem-vindo:

##### Endpoint: /

##### Método: GET

Retorna uma mensagem de boas-vindas ao robo crawler do ESAJ Alagoas e Ceará. Use o método POST para buscar informações usando o número do processo.

---

#### Buscar Processo:

##### Endpoint: /

##### Método: POST

Descrição: Busca informações sobre um processo com base no número do processo fornecido.

Parâmetro:

- numero_processo (string): O número do processo a ser pesquisado.

O número do processo deve seguir o padrão CNJ de numeração de processos jurídicos: NNNNNNN-DD.AAAA.JTR.OOOO

Exemplo de requisição:

```json
{
  "numero_processo": "0705244-63.2022.8.02.0001"
}
```

---

#### Listar Tribunais:

##### Endpoint: /tribunais

##### Método: GET

Retorna uma lista com todos os tribunais disponíveis no crawler.

---

#### Buscar Tribunal por ID:

##### Endpoint: /tribunais/{tribunal_id}

##### Método: GET

Busca um tribunal pelo seu ID.
Parâmetro:

- tribunal_id (string): O ID do tribunal a ser buscado.

---

#### Adicionar Tribunal:

##### Endpoint: /tribunais

##### Método: POST

Adiciona um novo tribunal à lista de tribunais.
Parâmetro:

- objeto da classe Tribunal:
  - tribunal_id (string): O ID do tribunal a ser adicionado.
  - uf (string): sigla UF do estado em questão
  - base_url (string): radical da url do esaj correspondete ao tribunal

Exemplo de requisição:

```json
{
  "tribunal_id": "06",
  "uf": "CE",
  "base_url": "https://esaj.tjce.jus.br"
}
```

---

#### Deletar Tribunal

##### Endpoint: /tribunais/{tribunal_id}

##### Método: DELETE

Deleta um tribunal da lista de tribunais.
Parâmetro:

- tribunal_id (string): O ID do tribunal a ser deletado.
