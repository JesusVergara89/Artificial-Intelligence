import re
import nltk
import urllib.request
from inscriptis import get_text
import heapq
from googletrans import Translator

# Asegúrate de que los recursos necesarios de NLTK estén descargados
nltk.download('punkt')
nltk.download('stopwords')

# Scrapping text from the source
link = "https://es.wikipedia.org/wiki/Magia"
html = urllib.request.urlopen(link).read().decode('utf-8')
text = get_text(html)
article_text = text.replace("[ edit ]", "")
print("###########")

# Procesamiento de texto
article_text = re.sub(r'[\[[0-9]]\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('english')

# Calcular frecuencias de palabras
word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word.lower() not in stopwords:
        if word.lower() not in word_frequencies:
            word_frequencies[word.lower()] = 1
        else: 
            word_frequencies[word.lower()] += 1

maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / maximum_frequency

# Puntuar oraciones
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[word]
                else: 
                    sentence_scores[sent] += word_frequencies[word]

# Resumen
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)

# Traducción
translator = Translator()
translate = translator.translate(summary, src='es', dest='en')
print(translate.text)
