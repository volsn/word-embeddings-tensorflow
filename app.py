from flask import Flask, render_template, request
import json
import pickle

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras import layers, Sequential
from keras.utils import to_categorical
from keras.initializers import Constant

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/articles/all/')
def articles_all():
    with open('buzzfeed.json', 'r') as f:
        articles = json.load(f)

    return render_template('articles.html', articles=articles, articles_count=len(articles), category_name='Все Статьи')

@app.route('/articles/cat/<category_name>')
def articles_category(category_name=None):
    with open('buzzfeed.json', 'r') as f:
        articles = json.load(f)

    output = []
    for article in articles:
        if article['category'] == category_name.lower():
            output.append({
                'id': article['id'],
                'title': article['title'],
                'link': article['link'],
                'summary': article['summary'],
                'text': article['text']
            })

    return render_template('articles.html', articles=output, articles_count=len(output), category_name=category_name.capitalize())

@app.route('/articles/single/<id>/')
def articles_single(id=None):
    with open('buzzfeed.json', 'r') as f:
        articles = json.load(f)

    for article in articles:
        if article['id'] == int(id):
            return render_template('article.html', article=article)

    return render_template('404.html', id=id)

@app.route('/classifier/', methods=['POST'])
def output():
    input = request.form['text-input']
    with open('tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

    sequences = tokenizer.texts_to_sequences([input])
    MAX_SEQUENCE_LENGTH = 200
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

    classifier = load_model('model.h5')
    classifier.predict(data)

    return render_template('classifier.html', output=input)
