from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/articles/all/')
def articles_all():
    dataset = pd.read_csv('dataset.csv')

    articles = []
    for i, (title, href, type, text) in dataset.iterrows():
        articles.append({
            'pk': i,
            'title': title,
            'type': type,
            'href': href,
            'text': text
        })

    return render_template('articles.html', articles=articles)

@app.route('/articles/<pk>/')
def articles_single(pk=None):
    dataset = pd.read_csv('dataset.csv')
    article = {
        'title': dataset.iloc[int(pk)].title,
        'text': dataset.iloc[int(pk)].text,
    }

    return render_template('article.html', article=article)

@app.route('/output/', methods=['GET', 'POST'])
def output():
     text = request.form['TextArea']
     return render_template('output.html', output=text)
