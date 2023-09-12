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

def getSonho(dataFrame):
    sonho = dataFrame['Escreva algumas linhas sobre sua história e seus sonhos de vida.']
    textoSonho = sonho.str.cat(sep = ' ')
    docSonho = nlp(textoSonho, disable = ['ner'])
    wordsSonho = [token.lemma_ for token in docSonho if not token.is_punct and not token.is_stop and not token.is_space]
    freqSonho = Counter(wordsSonho)
    print(freqSonho)
    matcher = Matcher(nlp.vocab) 
    pattern = [{'POS':('ADJ')}, {'POS':'NOUN'}]
    matcher.add('ADJ_PHRASE', [pattern]) 
    matches = matcher(docSonho, as_spans=True) 
    phrases = [] 
    for span in matches:
        phrases.append(span.text.lower())
        phrase_freq = Counter(phrases)
    print(phrase_freq)

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
    emprego = dataFrame['Empregos Tratados']
    df = pd.DataFrame(emprego)
    df['Empregos Tratados'] = df['Empregos Tratados'].apply(lambda x: preprocess_text(x))
    df = df.dropna(subset=['Empregos Tratados'])
    company_counts = Counter()

    for index, row in df.iterrows():
        company_counts.update(row['Empregos Tratados'])

    company_list = [(company, count) for company, count in company_counts.items()]

    company_list.sort(key=lambda x: x[1], reverse=True)

    for company, count in company_list:
        print(f"({company}, {count})")

def checaSimilar(dataFrame):
    emprego = dataFrame[dataFrame['Empregos Tratados'].notnull()]
    thereshold = 0.80
    empresasSimilares = []
    k= 0 
    for i, empresa1 in enumerate(emprego[:-1]):
        j = emprego.index[k]
        for empresa2 in emprego[j+1]:
            if empresa1 != '' and empresa2 != '':
                similaridade = SequenceMatcher(None, empresa1, empresa2).ratio()
                if similaridade > thereshold:
                    dataFrame['Empregos Tratados'] = dataFrame['Empregos Tratados'].str.replace(empresa1, empresa2)
                    empresasSimilares.append(empresa1, empresa2, similaridade)
        
        k += 1



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
    print(colunaEmprego)

nlp = spacy.load('pt_core_news_sm')
nlp.max_length = 1850000
dataFrame = pd.read_excel('perfilNovo.xlsx')

nltk.download('punkt')
criaColunaEmprego(dataFrame)
checaSimilar(dataFrame)
contagemEmprego(dataFrame)
#getSonho(dataFrame)
#getEmprego(dataFrame)
#pattern2 = [{'POS':'NOUN' or 'ADJ'}, {'POS':'PROPN'}]
