from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
import pickle

#the top hundred words.
vectorizer = CountVectorizer(max_features=1000, stop_words={"english"})
X = vectorizer.fit_transform(news_train_df['headline'].values)
path_vectorizer = 'vectorizer.pkl'
pickle.dump(vectorizer, open(path_vectorizer, 'wb'))


tf_transformer = TfidfTransformer(use_idf=False)
X_train_tf = tf_transformer.fit_transform(X)
path_tf_transformer = 'tf_transformer.pkl'
pickle.dump(tf_transformer, open(path_tf_transformer, 'wb'))