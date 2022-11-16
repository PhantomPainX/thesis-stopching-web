from nltk.stem.porter import PorterStemmer
import nltk, re
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class AIUtils:
    
    def stemming(self, content):
        nltk.download('stopwords')
        nltk.download('punkt')
        stop_words = set(stopwords.words('spanish'))
        port_stem = PorterStemmer()

        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stop_words]
        stemmed_content = ' '.join(stemmed_content)
        return stemmed_content

    def vectorize(self, content):
        vectorizer = TfidfVectorizer()