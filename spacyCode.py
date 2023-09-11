import spacy
import pandas as pd
from collections import Counter
from spacy.matcher import Matcher 

nlp = spacy.load('pt_core_news_sm')
nlp.max_length = 1850000
dataFrame = pd.read_excel('perfilNovo.xlsx')
sonho = dataFrame['Escreva algumas linhas sobre sua história e seus sonhos de vida.']
emprego = dataFrame['Qual empresa que você está contratado agora?']
texto = sonho.str.cat(sep = ' ')
textoEmprego = emprego.str.cat(sep = ' ')
docEmprego = nlp(textoEmprego, disable= ['ner'])
docSonho = nlp(texto, disable = ['ner'])

words = [token.lemma_ for token in docSonho if not token.is_punct and not token.is_stop and not token.is_space]
wordsEmprego =  [token.lemma_ for token in docEmprego if not token.is_stop and not token.is_punct and not token.is_space]
word_freq = Counter(words) 
#print(word_freq.most_common(20))
wordFreqEmprego = Counter(wordsEmprego)
#print(wordFreqEmprego)

matcher = Matcher(nlp.vocab) 
pattern = [{'POS':('ADJ')}, {'POS':'NOUN'}] 
pattern2 = [{'POS':'NOUN' or 'ADJ'}, {'POS':'PROPN'}]
matcher.add('ADJ_PHRASE', [pattern]) 
matches = matcher(docSonho, as_spans=True) 
phrases = [] 
for span in matches:
    phrases.append(span.text.lower())
    phrase_freq = Counter(phrases)
print(phrase_freq)