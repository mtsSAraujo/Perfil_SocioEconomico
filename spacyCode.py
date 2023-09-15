import spacy
import pandas as pd
from collections import Counter
from spacy.matcher import Matcher
import unicodedata
import nltk
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('portuguese'))
nlp = spacy.load("pt_core_news_sm")
nlp.max_length = 1850000

def getSonho(dataFrame):
    sonho = dataFrame['Escreva algumas linhas sobre sua história e seus sonhos de vida.']
    textoSonho = sonho.str.cat(sep = ' ')
    docSonho = nlp(textoSonho, disable = ['ner'])
    wordsSonho = [token.lemma_ for token in docSonho if not token.is_punct and not token.is_stop and not token.is_space]
    freqSonho = Counter(wordsSonho)
    #print(freqSonho)
    matcher = Matcher(nlp.vocab)
    pattern2 = [{'LOWER': {'IN' : ['aprender', 'desenvolver','trabalhar', 'viajar', 'gastar', 'obter', 'ganhar', 'adquirir', 'conhecer', 'mudar', 'ser', 'conseguir', 'conquistar', 'receber']}}, {'IS_ALPHA':True, 'OP':'?'},
    {'IS_ALPHA':True, 'OP':'?'}, {'POS':'NOUN'}]
    matcher.add('ADJ_PHRASE', [pattern2]) 
    matches = matcher(docSonho, as_spans=True) 
    phrases = [] 
    listaElementos= []
    for span in matches:
        phrases.append(span.text.lower())
        phrase_freq = Counter(phrases)     
    print(phrase_freq)
    series = pd.Series(phrases)
    dataFrame['Sonhos mais recorrentes'] = series
    dataFrame = checaSimilaridade(dataFrame)
    return(dataFrame)

def checaSimilaridade(dataFrame):
    sonho = dataFrame[dataFrame['Sonhos mais recorrentes'].notnull()]
    colunaSonho = sonho['Sonhos mais recorrentes']
    #print(colunaEmprego)
    thereshold = 0.80
    empresasSimilares = []
    for i, sonho1 in enumerate(colunaSonho):
        for j, sonho2 in enumerate(colunaSonho):
            if i < j and sonho1 != '' and sonho2 != '':
                similaridade = SequenceMatcher(None, sonho1, sonho2).ratio()
                if similaridade > thereshold:
                    dataFrame['Sonhos mais recorrentes'] = dataFrame['Sonhos mais recorrentes'].str.replace(sonho2, sonho1)
                    empresasSimilares.append((sonho1, sonho2, similaridade))
                    print(f'indice i: {i} , valor: {sonho1}, \n indice j: {j}, valor: {sonho2} \n Similaridade: {similaridade}')

    return(dataFrame)

def criaColunaSonhos():
    a = 0

'''def getEmprego(dataFrame):
    emprego = dataFrame['Empregos Tratados']
    print(emprego[1])
    textoEmprego = emprego.str.cat(sep = ' ')
    docEmprego = nlp(textoEmprego, disable= ['ner'])
    freqEmprego = Counter(docEmprego)
    print(freqEmprego.most_common(30))
    matcher = Matcher(nlp.vocab) 
    pattern = [{'POS':('NOUN' or "ADJ")}]
    matcher.add('ADJ_PHRASE', [pattern]) 
    matches = matcher(docEmprego, as_spans=True) 
    phrases = [] 
    for span in matches:
        phrases.append(span.text.lower())
        phrase_freq = Counter(phrases)
    print(phrase_freq)'''

def preprocess_text(text):
    if isinstance(text, str):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
        return tokens
    return [] 

def contagemEmprego(dataFrame):

    emprego_column = 'Empregos Tratados'

    # Remova linhas com valores nulos na coluna de empregos
    dataFrame_cleaned = dataFrame.dropna(subset=[emprego_column])

    # Contagem de empregos inteiros
    company_counts = Counter(dataFrame_cleaned[emprego_column])

    # Contagem de linhas sem informações
    desempregados = dataFrame[~dataFrame.index.isin(dataFrame_cleaned.index)].shape[0]

    # Transformando o resultado em uma lista de tuplas (empresa, contagem)
    company_list = [(company, count) for company, count in company_counts.items()]

    # Classificando as empresas por contagem em ordem decrescente
    company_list.sort(key=lambda x: x[1], reverse=True)

    for company, count in company_list:
        print(f"({company}, {count})")

    print(f"Desempregados: {desempregados}")

#nlp = spacy.load('pt_core_news_sm')
#nlp.max_length = 1850000

nltk.download('punkt')
#contagemEmprego(dataFrameTratado)
#getSonho(dataFrameTratado)
#getEmprego(dataFrameTratado)