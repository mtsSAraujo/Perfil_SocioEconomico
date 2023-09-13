import pandas as pd
import unicodedata
from difflib import SequenceMatcher
from spacyCode import getSonho


dataFrame = pd.read_excel('perfil.xlsx')

def tratamentoDeDados():
    trataMesNascimento()
    trataJornal()
    trataPlanoDeSaude()
    criaColunaEmprego(dataFrame)
    dataFrame.drop(['Mês de nascimento', 'Mês de nascimento2'], axis = 1, inplace=True)
    dataFrame.drop(['Você tem plano de saúde privado?2'], axis = 1, inplace=True)
    dataFrame.drop(['TV2', 'Internet2', 'Revistas2', 'Rádio3', 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2', 'Conversas informais com amigos2'], axis = 1, inplace=True)
    dataFrame.drop(['Hora de início', 'Hora de conclusão', 'ID', 'Email', 'Hora da última modificação'], axis = 1, inplace=True)
    dataFrame.to_excel('perfilNovo.xlsx', index = False)
    dataFrameNovo = pd.read_excel('perfilNovo.xlsx')
    checaSimilar(dataFrameNovo)
    getSonho(dataFrameNovo)
    dataFrameNovo.to_excel('perfilNovo.xlsx')


def criaColunaEmprego(dataFrame):
    emprego = dataFrame[dataFrame['Qual empresa que você está contratado agora?'].notnull()]
    colunaEmprego = emprego['Qual empresa que você está contratado agora?']
    k = 0
    chars = '.,!?-/\|:;^~`[]*&¨%$#@()'
    for i in (colunaEmprego):
        j = colunaEmprego.index[k]
        i = i.lower()
        processamento = unicodedata.normalize("NFD", i)
        processamento = processamento.encode("ascii", "ignore")
        processamento = processamento.decode("utf-8")
        processamento = processamento.translate(str.maketrans('', '', chars))
        processamento = processamento.strip()
        colunaEmprego[j] = processamento
        k +=  1

    dataFrame['Empregos Tratados'] = colunaEmprego
    return dataFrame

def checaSimilar(dataFrame):
    emprego = dataFrame[dataFrame['Empregos Tratados'].notnull()]
    colunaEmprego = emprego['Empregos Tratados']
    #print(colunaEmprego)
    thereshold = 0.80
    empresasSimilares = []
    for i, empresa1 in enumerate(colunaEmprego):
        for j, empresa2 in enumerate(colunaEmprego):
            if i < j and empresa1 != '' and empresa2 != '':
                similaridade = SequenceMatcher(None, empresa1, empresa2).ratio()
                if similaridade > thereshold:
                    dataFrame['Empregos Tratados'] = dataFrame['Empregos Tratados'].str.replace(empresa1, empresa2)
                    empresasSimilares.append((empresa1, empresa2, similaridade))
                    print(f'indice i: {i} , valor: {empresa1}, \n indice j: {j}, valor: {empresa2}')

def trataMesNascimento():

    coluna = dataFrame[dataFrame['Mês de nascimento'].notnull()]
    mesNascimento = coluna['Mês de nascimento']
    k = 0
    for i in mesNascimento:
        j = mesNascimento.index[k]
        dataFrame.iat[j, 16] = i
        k = k + 1

    coluna = dataFrame[dataFrame['Mês de nascimento2'].notnull()]
    mesNascimento = coluna['Mês de nascimento2']
    k = 0
    for i in mesNascimento:
        j = mesNascimento.index[k]
        dataFrame.iat[j, 16] = i
        k = k + 1


def trataJornal():
    coluna = dataFrame[dataFrame['TV'].isnull()]
    TV = coluna['TV2']
    internet = coluna['Internet2']
    revistas = coluna['Revistas2']
    radio2 = coluna['Rádio3']
    redesSociais = coluna['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2']
    conversasInformais = coluna['Conversas informais com amigos2']
    k = 0
    for i in TV:
        j = TV.index[k]
        dataFrame.iat[j, 76] = i
        k = k + 1

    k = 0
    for i in internet:
        j = internet.index[k]
        dataFrame.iat[j, 77] = i
        k = k + 1

    k = 0
    for i in revistas:
        j = revistas.index[k]
        dataFrame.iat[j, 78] = i
        k = k + 1

    k = 0
    for i in radio2:
        j = radio2.index[k]
        dataFrame.iat[j, 79] = i
        k = k + 1

    k = 0
    for i in redesSociais:
        j = redesSociais.index[k]
        dataFrame.iat[j, 80] = i
        k = k + 1

    k = 0
    for i in conversasInformais:
        j = conversasInformais.index[k]
        dataFrame.iat[j, 81] = i
        k = k + 1

def trataPlanoDeSaude():
    coluna = dataFrame[dataFrame['Você tem plano de saúde privado?2'].notnull()]
    planoDeSaude = coluna['Você tem plano de saúde privado?2']
    k = 0
    for i in planoDeSaude:
        j = planoDeSaude.index[k]
        dataFrame.iat[j, 46] = i
        k = k + 1
