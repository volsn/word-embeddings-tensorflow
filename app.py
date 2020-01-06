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
            'id': i,
            'header': title,
            'type': type,
            'href': href,
            'description': ' '.join(text.split('.')[:3]).replace('\n', ''),
            'text': text
        })

    return render_template('articles.html', articles=articles, articles_count=len(articles), category_name='Все Статьи')

@app.route('/articles/cat/<category_name>')
def articles_category(category_name=None):
    dataset = pd.read_csv('dataset.csv')

    articles = []
    for i, (title, href, type, text) in dataset.iterrows():
        if type == category_name.lower():
            articles.append({
                'id': i,
                'header': title,
                'type': type,
                'href': href,
                'description': text[:250],
                'text': text
            })

    return render_template('articles.html', articles=articles, articles_count=len(articles), category_name=category_name.capitalize())

@app.route('/articles/<id>/')
def articles_single(id=None):
    dataset = pd.read_csv('dataset.csv')
    article = {
        'id': id,
        'title': dataset.iloc[int(id)].title,
        'text': dataset.iloc[int(id)].text,
    }

    return render_template('article.html', article=article)

@app.route('/output/', methods=['GET', 'POST'])
def output():
     text = request.form['TextArea']
     return render_template('output.html', output=text)
