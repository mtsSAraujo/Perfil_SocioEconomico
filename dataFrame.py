import pandas as pd
import numpy as np

dataFrame = pd.read_excel('perfil.xlsx')

def tratamentoDeDados():
    trataMesNascimento()
    trataJornal()
    trataPlanoDeSaude()
    dataFrame.drop(['Mês de nascimento', 'Mês de nascimento2'], axis = 1, inplace=True)
    dataFrame.drop(['Você tem plano de saúde privado?2'], axis = 1, inplace=True)
    dataFrame.drop(['TV2', 'Internet2', 'Revistas2', 'Rádio3', 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2', 'Conversas informais com amigos2'], axis = 1, inplace=True)
    dataFrame.to_excel('perfilNovo.xlsx', index = False)

def trataMesNascimento():

    coluna = dataFrame[dataFrame['Mês de nascimento'].notnull()]
    mesNascimento = coluna['Mês de nascimento']
    k = 0
    print("fazendo metodo 1")
    for i in mesNascimento:
        j = mesNascimento.index[k]
        dataFrame.iat[j, 16] = i
        k = k + 1

    coluna = dataFrame[dataFrame['Mês de nascimento2'].notnull()]
    mesNascimento = coluna['Mês de nascimento2']
    k = 0
    print("fazendo metodo 2")
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
