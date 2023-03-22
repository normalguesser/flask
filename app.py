from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime
import os
import random

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nrdl_user:WObWv7aoBHeI5ilj1ePdyAemX0RKQoct@dpg-cgdo3mm4dadbr0si98ng-a/nrdl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

class MovieBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    diml_rate = db.Column(db.Integer, default=0)
    nast_rate = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

class SerialBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    diml_rate = db.Column(db.Integer, default=0)
    nast_rate = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

class MovieToWatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    next_movie = db.Column(db.String(200), nullable=False)

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
            return 'Помилка: не вдалось додати.'

    else:
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()
        return render_template('add.html', movies=moviesToWatch)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        
        movie_content = request.form['content']
        movie_diml_rate = request.form['diml_rate']
        movie_nast_rate = request.form['nast_rate']

        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie_diml_rate == "":
            movie_diml_rate = '0'
        if int(movie_diml_rate) > 11:
            movie_diml_rate = '10'
        if int(movie_diml_rate) < 0:
            movie_diml_rate = '0'

        if movie_nast_rate == "":
            movie_nast_rate = '0'
        if int(movie_nast_rate) > 11:
            movie_nast_rate = '10'
        if int(movie_nast_rate) < 0:
            movie_nast_rate = '0'

        new_movie = MovieBase(content=movie_content, diml_rate=movie_diml_rate, nast_rate=movie_nast_rate)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати.'

    else:
        movies = MovieBase.query.order_by(MovieBase.id.desc()).all()
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()

        return render_template('index.html', movies=movies, moviesToWatch=moviesToWatch)

@app.route('/serials', methods=['POST', 'GET'])
def serials():
    if request.method == 'POST':
        
        movie_content = request.form['content']
        movie_diml_rate = request.form['diml_rate']
        movie_nast_rate = request.form['nast_rate']

        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie_diml_rate == "":
            movie_diml_rate = '0'
        if int(movie_diml_rate) > 11:
            movie_diml_rate = '10'
        if int(movie_diml_rate) < 0:
            movie_diml_rate = '0'

        if movie_nast_rate == "":
            movie_nast_rate = '0'
        if int(movie_nast_rate) > 11:
            movie_nast_rate = '10'
        if int(movie_nast_rate) < 0:
            movie_nast_rate = '0'

        new_movie = SerialBase(content=movie_content, diml_rate=movie_diml_rate, nast_rate=movie_nast_rate)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/serials')
        except:
            return 'Помилка: не вдалось додати.'

    else:
        movies = SerialBase.query.order_by(SerialBase.id.desc()).all()
        moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()

        return render_template('serials.html', movies=movies, moviesToWatch=moviesToWatch)

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
        movie.nast_rate = request.form['nast_rate']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie.diml_rate == "":
            movie.diml_rate = '0'
        if int(movie.diml_rate) > 11:
            movie.diml_rate = '10'
        if int(movie.diml_rate) < 0:
            movie.diml_rate = '0'

        if movie.nast_rate == "":
            movie.nast_rate = '0'
        if int(movie.nast_rate) > 11:
            movie.nast_rate = '10'
        if int(movie.nast_rate) < 0:
            movie.nast_rate = '0'

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось оновити.'

    else:
        return render_template('update.html', movie=movie)

@app.route('/updates/<int:id>', methods=['GET', 'POST'])
def updates(id):
    movie = SerialBase.query.get_or_404(id)

    if request.method == 'POST':
        movie.content = request.form['content']
        movie.diml_rate = request.form['diml_rate']
        movie.nast_rate = request.form['nast_rate']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'

        if movie.diml_rate == "":
            movie.diml_rate = '0'
        if int(movie.diml_rate) > 11:
            movie.diml_rate = '10'
        if int(movie.diml_rate) < 0:
            movie.diml_rate = '0'

        if movie.nast_rate == "":
            movie.nast_rate = '0'
        if int(movie.nast_rate) > 11:
            movie.nast_rate = '10'
        if int(movie.nast_rate) < 0:
            movie.nast_rate = '0'

        try:
            db.session.commit()
            return redirect('/serials')
        except:
            return 'Помилка: не вдалось оновити.'

    else:
        return render_template('updates.html', movie=movie)

@app.route('/random')
def randomMovie():
    moviesToWatch = MovieToWatch.query.order_by(MovieToWatch.id.desc()).all()
    if len(moviesToWatch) > 0:
        movie = random.choice(moviesToWatch)
        return render_template('random.html', movie=movie)
    else:
        return 'Список фільмів для вибору порожній'

if __name__ == "__main__":
    app.run(debug=True)
