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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gatzcodxeaneds:24fedfa6f8bb30c44c8d0cf05e20a05a8c641f10f81830e75f764cb6d6bbad66@ec2-54-224-120-186.compute-1.amazonaws.com:5432/dk1n1n9o95jk2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

class MovieBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dio_rate = db.Column(db.Integer, default=0)
    andrew_rate = db.Column(db.Integer, default=0)
    dima_rate = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

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
        movie_dio_rate = request.form['dio_rate']
        movie_andrew_rate = request.form['andrew_rate']
        movie_dima_rate = request.form['dima_rate']
        
        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
        
        if int(movie_dio_rate) > 11:
            movie_dio_rate = '10'
        if int(movie_dio_rate) < 0:
            movie_dio_rate = '0'
            
        if int(movie_andrew_rate) > 11:
            movie_andrew_rate = '10'
        if int(movie_andrew_rate) < 0:
            movie_andrew_rate = '0'

        if int(movie_dima_rate) > 11:
            movie_dima_rate = '10'
        if int(movie_dima_rate) < 0:
            movie_dima_rate = '0'
        
        new_movie = MovieBase(content=movie_content, dio_rate=movie_dio_rate, andrew_rate=movie_andrew_rate, dima_rate=movie_dima_rate)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'Помилка: не вдалось додати фiльм.'

    else:
        movies = MovieBase.query.order_by(MovieBase.date_created.desc()).all()
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
        movie.dio_rate = request.form['dio_rate']
        movie.andrew_rate = request.form['andrew_rate']
        movie.dima_rate = request.form['dima_rate']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
        
        if int(movie.dio_rate) > 11:
            movie.dio_rate = '10'
        if int(movie.dio_rate) < 0:
            movie.dio_rate = '0'
            
        if int(movie.andrew_rate) > 11:
            movie.andrew_rate = '10'
        if int(movie.andrew_rate) < 0:
            movie.andrew_rate = '0'

        if int(movie.dima_rate) > 11:
            movie.dima_rate = '10'
        if int(movie.dima_rate) < 0:
            movie.dima_rate = '0'

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
