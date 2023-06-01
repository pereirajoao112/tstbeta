import time
import requests
import openai

# Configurar o token de acesso do OpenAI
openai.api_key = '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'

# Configurar o token de acesso da API do Mercado Livre
token_acesso_mercado_livre = 'APP_USR-2040840384352859-053010-af539d655ca0f44f080f280680a605af-199749897'


# Função para obter a lista de produtos do Mercado Livre
def obter_produtos_mercado_livre():
    url = f'https://api.mercadolibre.com/users/199749897/items/search?access_token={token_acesso_mercado_livre}'

    response = requests.get(url)
    produtos = response.json()

    return produtos["results"]

# Função para obter as perguntas de um produto
def obter_perguntas_produto(id_produto):
    url = f'https://api.mercadolibre.com/questions/search?item_id={id_produto}&access_token={token_acesso_mercado_livre}'

    response = requests.get(url)
    perguntas = response.json()

    return perguntas['questions']

# Função para obter os detalhes de um produto
def obter_detalhes_produto(id_produto):
    url = f'https://api.mercadolibre.com/items/{id_produto}'

    response = requests.get(url)
    detalhes = response.json()

    return detalhes['title']
    return detalhes['condition']
    return detalhes['value_name']
    return detalhes['value_id']

# Função para responder uma pergunta usando o Chat GPT, levando em consideração o título do produto
def responder_pergunta(pergunta, titulo_produto):
    prompt = f"Responder como se fosse um vendedor do mercado livre, se estiverem perguntando se envia hoje, dizer que após as 12h o envio é realizado apenas no proximo dia, e conforme o seguinte produto: {titulo_produto}: {pergunta}"

    resposta = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )

    return resposta.choices[0].text.strip()

# Função para enviar a resposta da pergunta para o Mercado Livre
def enviar_resposta_pergunta(id_pergunta, resposta):
    url = f'https://api.mercadolibre.com/answers?access_token={token_acesso_mercado_livre}'
    payload = {
        'question_id': id_pergunta,
        'text': resposta
    }

    response = requests.post(url, json=payload)
    resposta_enviada = response.json()

    return resposta_enviada

# Loop infinito para manter o código em execução
while True:
    # Obter a lista de produtos
    produtos = obter_produtos_mercado_livre()

    # Iterar sobre cada produto
    for produto_id in produtos:
        id_produto = produto_id

        # Obter os detalhes do produto, incluindo o título
        titulo_produto = obter_detalhes_produto(id_produto)

        perguntas = obter_perguntas_produto(id_produto)

        # Iterar sobre cada pergunta do produto
        for pergunta in perguntas:
            id_pergunta = pergunta['id']
            texto_pergunta = pergunta['text']

            # Responder a pergunta usando o Chat GPT, levando em consideração o título do produto
            resposta = responder_pergunta(texto_pergunta, titulo_produto)

            # Enviar a resposta da pergunta para o Mercado Livre
            resposta_enviada = enviar_resposta_pergunta(id_pergunta, resposta)

            # Verificar se a resposta foi enviada com sucesso
            if 'id' in resposta_enviada:
                print('Pergunta:', texto_pergunta)
                print('Resposta:', resposta)
                print('Resposta enviada com sucesso!')
                #print()
            else:
                print('Ocorreu um erro ao enviar a resposta da pergunta:')
                print(resposta_enviada)
                #print()












#import openai

# Defina sua chave de API do OpenAI
#openai.api_key = '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'

#def obter_resposta_pergunta(pergunta):
    #response = openai.Completion.create(
        #engine='text-davinci-003',
        #prompt=pergunta,
       # max_tokens=50,
      #  n=1,
     #   temperature=0.7,
    #)

    #if response.choices:
   #     return response.choices[0].text.strip()
  #  else:
 #       return "Desculpe, não consegui gerar uma resposta para sua pergunta."

# Pergunta do usuário
#pergunta = input("Digite sua pergunta: ")

# Obter a resposta usando a função
#resposta = obter_resposta_pergunta(pergunta)

# Imprimir a pergunta e a resposta
#print("Pergunta:", pergunta)
#print("Resposta:", resposta)
