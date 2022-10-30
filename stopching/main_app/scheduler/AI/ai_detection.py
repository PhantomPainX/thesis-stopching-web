import pandas as pd
import pickle, os, sklearn, nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from main_app.scheduler.AI.ai_utils import AIUtils
from sklearn import *

#get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

class AIDetection(AIUtils):

  def __init__(self):
    self.LRModel = pickle.load(open(current_dir + '/LRModel.sav', 'rb'))

  def LRModel_Predict(self, text):
    testing_news = {'text': [text]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(self.stemming)
    new_x_test = new_def_test["text"]
    model_vectorizer = pickle.load(open(current_dir + '/LRModelVectorizer.sav', 'rb'))
    new_xv_test = model_vectorizer.transform(new_x_test)
    pred = self.LRModel.predict(new_xv_test)
    prob = self.LRModel.predict_proba(new_xv_test)

    #aproximate the probability to 2 decimals

    return {
      'prediction_label': pred[0],
      'prediction_name': 'Fake' if pred[0] == 1 else 'Real',
      'probability': prob[0][1],
      'percent_probability': round(prob[0][1], 2) * 100
    }


# ai = AIDetection("Hubo una estampida de personas en Corea del Sur, debido a las fiestas de Halloween, más de 100,000 personas asistieron a Itaewon. Las autoridades comenzaron a recibir al menos 80 llamadas pidiendo ayuda y al parecer al rededor de 50 personas sufrieron un paro cardíaco")
# result = ai.LRModel_Predict()
# print(result)