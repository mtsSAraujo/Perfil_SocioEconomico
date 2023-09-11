import spacy
import pandas as pd
from collections import Counter
from spacy.matcher import Matcher 

def getSonho(dataFrame):
    sonho = dataFrame['Escreva algumas linhas sobre sua história e seus sonhos de vida.']
    textoSonho = sonho.str.cat(sep = ' ')
    docSonho = nlp(textoSonho, disable = ['ner'])
    wordsSonho = [token.lemma_ for token in docSonho if not token.is_punct and not token.is_stop and not token.is_space]
    freqSonho = Counter(wordsSonho)
    print(freqSonho)
    matcher = Matcher(nlp.vocab) 
    pattern = [{'POS':('VERB')}, {'POS':'NOUN'}]
    matcher.add('ADJ_PHRASE', [pattern]) 
    matches = matcher(docSonho, as_spans=True) 
    phrases = [] 
    for span in matches:
        phrases.append(span.text.lower())
        phrase_freq = Counter(phrases)
    print(phrase_freq)

def getEmprego(dataFrame):
    emprego = dataFrame['Qual empresa que você está contratado agora?']
    textoEmprego = emprego.str.cat(sep = ' ')
    docEmprego = nlp(textoEmprego, disable= ['ner'])
    freqEmprego = Counter(docEmprego)
    print(freqEmprego.most_common(30))
    matcher = Matcher(nlp.vocab) 
    pattern = [{'POS':('NOUN')}, {'POS':'NOUN'}]
    matcher.add('ADJ_PHRASE', [pattern]) 
    matches = matcher(docEmprego, as_spans=True) 
    phrases = [] 
    for span in matches:
        phrases.append(span.text.lower())
        phrase_freq = Counter(phrases)
    #print(phrase_freq)

nlp = spacy.load('pt_core_news_sm')
nlp.max_length = 1850000
dataFrame = pd.read_excel('perfilNovo.xlsx')

#getSonho(dataFrame)
getEmprego(dataFrame)

#pattern2 = [{'POS':'NOUN' or 'ADJ'}, {'POS':'PROPN'}]
