from Códigos import codigos
from os import path


def Leitor_de_Arquivos(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='latin1') as arquivo:
            conteudo = arquivo.read()
        return conteudo

    except Exception as e:
        return f"Erro: {str(e)}"


def Tradutor_de_Códigos(texto):
    cods = codigos
    pares = [texto[i:i+2] for i in range(0, 10, 2)]
    descrições = []

    for par in pares:
        if par in cods:
            descrições.append(cods[par])

    if descrições:
        texto_Formatado = " ".join(descrições)
    else:
        texto_Formatado = "Nenhum Código Foi Encontrado!"

    return texto_Formatado


def Tradutor_de_CNAB(conteudo):
    DISTANCIA = 241
    segmento_do_registro = 13
    inicio_nome = segmento_do_registro + 30
    fim_nome = inicio_nome + 30
    inicio_codigo = segmento_do_registro + 217
    fim_codigo = inicio_codigo + 10

    dados = []

    for _ in range(len(conteudo) // DISTANCIA):
        if conteudo[segmento_do_registro] == 'A':
            dados.append(f'Favorecido: {conteudo[inicio_nome:fim_nome].title()} Ocorrências: {
                conteudo[inicio_codigo:fim_codigo]} Descrições: {Tradutor_de_Códigos(conteudo[inicio_codigo:fim_codigo])}')

        segmento_do_registro += DISTANCIA
        inicio_nome += DISTANCIA
        fim_nome += DISTANCIA
        inicio_codigo += DISTANCIA
        fim_codigo += DISTANCIA

    return dados
