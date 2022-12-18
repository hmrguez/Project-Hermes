from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from Hermes import predict_text, predict_image


app = Flask(__name__)

class Query():

    def __init__(self, comment) -> None:
        predictions = predict_text(comment)

        self.content = comment
        self.toxic = predictions['toxic']
        self.severe_toxic = predictions['severe_toxic']
        self.obscene = predictions['obscene']
        self.threat = predictions['threat']
        self.insult = predictions['insult']
        self.identity_hate = predictions['identity_hate']

class IMGQuery():

    def __init__(self, img_path) -> None:
        
        self.path = img_path
        self.prediction = predict_image(img_path)


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        text_content = request.form['content']
        image_content = request.form['image_path']
        new_query_text = Query(text_content)
        
        if image_content != '':
            image_query = IMGQuery(image_content)
            return render_template('index.html', query = image_query, text_query = None)
        else:
            return render_template('index.html', query = None, text_query = new_query_text)
    else:
        return render_template('index.html', query = None, text_query = None)

if __name__ == "__main__":
    app.run(debug=True)