from flask import Flask, render_template, request, redirect, url_for
from application.forms import AddGame, AddRating, DeleteGame
from application import app, db
from application.models import GameRatings, Games


@app.route('/')
@app.route('/home')
def home():
    all_games = Games.query.all()
    output = ''
    return render_template("index.html", title="Home", all_games=all_games)
    

@app.route('/add_game', methods=["GET","POST"])
def add_game():
    form = AddGame()
    if request.method == "POST":
        if form.validate_on_submit():
                new_game = Games(
                    game_name=form.game_name.data, 
                    age_rating=form.age_rating.data,
                    genre=form.genre.data,
                    description=form.description.data
                )           
                db.session.add(new_game)
                db.session.commit()
                return redirect(url_for("home"))

    return render_template("add.html", title="Add a Game", form=form)

@app.route('/update', methods=["GET", "POST"])
def update():
    form = AddGame()
    update = Games.query.filter_by(game_name=form.game_name.data).first()
    if form.validate_on_submit():
        update.game_name = form.game_name.data
        update.age_rating = form.age_rating.data
        update.genre = form.genre.data
        update.description = form.description.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', title = 'Update Game Info', form=form, update=update)


@app.route('/add_rating', methods=["GET","POST"])
def add_rating():
    form = AddRating()
    if request.method == "POST":
        if form.validate_on_submit():
            game = Games.query.filter_by(game_name=form.game_name.data).first()
            new_rating = GameRatings(rating=form.rating.data)
            new_rating.game = game

            db.session.add(new_rating)
            db.session.commit()
            if GameRatings(rating=form.rating.data) is not None:
                rated = Games.query.filter_by(game_name=form.game_name.data).first()
                rated.rated = True
                db.session.add(rated)
                db.session.commit()
            return redirect(url_for("home"))

    return render_template("rating.html", title="Add a Rating", form=form)

@app.route('/delete_game', methods=["DELETE", "GET"])
def delete_game():
    form = DeleteGame()
    if request.method == "DELETE":
        if form.validate_on_submit():
            game_to_delete = Games.query.filter_by(game_name=form.game_name.data).first()
            db.session.delete(game_to_delete)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template('delete.html', title="Delete a game", form=form)

