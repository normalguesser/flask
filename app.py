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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lkvepagseawmgx:9ce6216230268ece23b4c0491ceed083a30062fc52d3aa96283c867605593446@ec2-34-232-191-133.compute-1.amazonaws.com:5432/dv3hh75la6ovr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

class MovieBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    nika_rate = db.Column(db.Integer, default=0)
    dima_rate = db.Column(db.Integer, default=0)
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
        movie_nika_rate = request.form['nika_rate']
        movie_dima_rate = request.form['dima_rate']
        movie_date_created = request.form['date_created']

        if movie_content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
        
        if int(movie_nika_rate) > 11:
            movie_nika_rate = '10'
        if int(movie_nika_rate) < 0:
            movie_nika_rate = '0'

        if int(movie_dima_rate) > 11:
            movie_dima_rate = '10'
        if int(movie_dima_rate) < 0:
            movie_dima_rate = '0'
        
        new_movie = MovieBase(content=movie_content, nika_rate=movie_nika_rate, dima_rate=movie_dima_rate, date_created=movie_date_created)

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
        movie.nika_rate = request.form['nika_rate']
        movie.dima_rate = request.form['dima_rate']
        movie.date_created = request.form['date_created']

        if movie.content == '':
            return 'Помилка: заголовок не повинен бути порожнiм.'
            
        if int(movie.nika_rate) > 11:
            movie.nika_rate = '10'
        if int(movie.nika_rate) < 0:
            movie.nika_rate = '0'

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
