from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os
import random

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tlmuqwpijnmuxs:cf4b7a10cf14ca508169a8de688ceba07b921b27918d5569d0fc0c071ed25c01@ec2-3-213-228-206.compute-1.amazonaws.com:5432/d6q9mkqft7bo7o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

class MovieBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    diml_rate = db.Column(db.Integer, default=0)
    dimo_rate = db.Column(db.Integer, default=0)
    andr_rate = db.Column(db.Integer, default=0)
    artm_rate = db.Column(db.Integer, default=0)
    maks_rate = db.Column(db.Integer, default=0)
    date_created = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

class MovieToWatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    next_movie = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        next_movie = request.form['next_movie']
        new_movie = MovieToWatch(next_movie=next_movie)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати фiльм.'

    else:
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.date_created.desc()).all()
        return render_template('add.html', movies=moviesToWatch)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        movie_content = request.form['content']
        movie_diml_rate = request.form['diml_rate']
        movie_dimo_rate = request.form['dimo_rate']
        movie_andr_rate = request.form['andr_rate']
        movie_artm_rate = request.form['artm_rate']
        movie_maks_rate = request.form['maks_rate']
        movie_date_created = request.form['date_created']

        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie_diml_rate == "":
            movie_diml_rate = '0'
        if int(movie_diml_rate) > 11:
            movie_diml_rate = '10'
        if int(movie_diml_rate) < 0:
            movie_diml_rate = '0'

        if movie_dimo_rate == "":
            movie_dimo_rate = '0'
        if int(movie_dimo_rate) > 11:
            movie_dimo_rate = '10'
        if int(movie_dimo_rate) < 0:
            movie_dimo_rate = '0'

        if movie_andr_rate == "":
            movie_andr_rate = '0'
        if int(movie_andr_rate) > 11:
            movie_andr_rate = '10'
        if int(movie_andr_rate) < 0:
            movie_andr_rate = '0'

        if movie_artm_rate == "":
            movie_artm_rate = '0'
        if int(movie_artm_rate) > 11:
            movie_artm_rate = '10'
        if int(movie_artm_rate) < 0:
            movie_artm_rate = '0'

        if movie_maks_rate == "":
            movie_maks_rate = '0'
        if int(movie_maks_rate) > 11:
            movie_maks_rate = '10'
        if int(movie_maks_rate) < 0:
            movie_maks_rate = '0'

        new_movie = MovieBase(content=movie_content, diml_rate=movie_diml_rate, dimo_rate=movie_dimo_rate, andr_rate=movie_andr_rate, artm_rate=movie_artm_rate, maks_rate=movie_maks_rate, date_created=movie_date_created)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати фiльм.'

    else:
        movies = MovieBase.query.order_by(MovieBase.id.desc()).all()
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.date_created.desc()).all()

        return render_template('index.html', movies=movies, moviesToWatch=moviesToWatch)

@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = MovieBase.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка: не вдалось видалити.'

@app.route('/deleteMovie/<int:id>')
def deleteMovie(id):
    movie_to_delete = MovieToWatch.query.get_or_404(id)

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Помилка: не вдалось видалити.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = MovieBase.query.get_or_404(id)

    if request.method == 'POST':
        movie.content = request.form['content']
        movie.diml_rate = request.form['diml_rate']
        movie.dimo_rate = request.form['dimo_rate']
        movie.andr_rate = request.form['andr_rate']
        movie.artm_rate = request.form['artm_rate']
        movie.maks_rate = request.form['maks_rate']
        movie.date_created = request.form['date_created']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie.diml_rate == "":
            movie.diml_rate = '0'
        if int(movie.diml_rate) > 11:
            movie.diml_rate = '10'
        if int(movie.diml_rate) < 0:
            movie.diml_rate = '0'

        if movie.dimo_rate == "":
            movie.dimo_rate = '0'
        if int(movie.dimo_rate) > 11:
            movie.dimo_rate = '10'
        if int(movie.dimo_rate) < 0:
            movie.dimo_rate = '0'

        if movie.andr_rate == "":
            movie.andr_rate = '0'
        if int(movie.andr_rate) > 11:
            movie.andr_rate = '10'
        if int(movie.andr_rate) < 0:
            movie.andr_rate = '0'

        if movie.artm_rate == "":
            movie.artm_rate = '0'
        if int(movie.artm_rate) > 11:
            movie.artm_rate = '10'
        if int(movie.artm_rate) < 0:
            movie.artm_rate = '0'

        if movie.maks_rate == "":
            movie.maks_rate = '0'
        if int(movie.maks_rate) > 11:
            movie.maks_rate = '10'
        if int(movie.maks_rate) < 0:
            movie.maks_rate = '0'

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось оновити.'

    else:
        return render_template('update.html', movie=movie)

@app.route('/random')
def randomMovie():
    moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.date_created.desc()).all()
    if len(moviesToWatch) > 0:
        movie = random.choice(moviesToWatch)
        return render_template('random.html', movie=movie)
    else:
        return 'Список фільмів для вибору порожній'

if __name__ == "__main__":
    app.run(debug=True)
