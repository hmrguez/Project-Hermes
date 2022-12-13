from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from Hermes import predict_text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Query(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    toxic = db.Column(db.Float, default = 0)
    severe_toxic = db.Column(db.Float, default = 0)
    obscene = db.Column(db.Float, default = 0)
    threat = db.Column(db.Float, default = 0)
    insult = db.Column(db.Float, default = 0)
    identity_hate = db.Column(db.Float, default = 0)

    # def __init__(self, comment) -> None:
    #     predictions = predict_text(comment)

    #     self.content = comment
    #     self.toxic = predictions['toxic']
    #     self.severe_toxic = predictions['severe_toxic']
    #     self.obscene = predictions['obscene']
    #     self.threat = predictions['threat']
    #     self.insult = predictions['insult']
    #     self.identity_hate = predictions['identity_hate']

    def __repr__(self) -> str:
        return '<QUERY %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        comment_content = request.form['content']
        new_query = Query(comment_content)
        
        try:
            # query_list.append(new_query)
            return redirect('/')
        except:
            return 'There was an issue uploading'

    # else:
        # return render_template('index.html', queries = query_list)

if __name__ == "__main__":
    app.run(debug=True)