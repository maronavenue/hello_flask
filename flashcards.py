import copy
import os

from flask import (Flask, render_template, abort, jsonify, request,
                    redirect, url_for, current_app, send_from_directory)
from model import DbStore

app = Flask(__name__)
with app.app_context():
    app.config['DB_STORE'] = DbStore()
dbh = app.config['DB_STORE']
print("Inside the app!")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        dbh.reset_db_and_load_seed_data()
        return redirect(url_for("welcome"))
    if request.method == "GET":
        cards = dbh.get_all_cards()
        return render_template("welcome.html", cards=cards)


@app.route("/card/<int:id>")
def card_view(id):
    cards = dbh.get_all_cards()
    curr_card = {}
    curr_index = 0
    for index, card in enumerate(cards):
        if id == card[0]:
            curr_card["id"], curr_card["question"], curr_card["answer"] = card
            curr_index = index
            break
    if not curr_card:
        abort(404)
    next_index = curr_index + 1 if curr_index != len(cards)-1 else 0

    return render_template("card.html", curr_card=curr_card, next_index=next_index, next_id=cards[next_index][0])


@app.route("/add_card/", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        question = request.form["question"].strip()
        answer = request.form["answer"].strip()
        if len(question) > 25:
            abort(400)
        if len(answer) > 25:
            abort(400)
        new_id = dbh.add_card(question, answer)
        return redirect(url_for("card_view", id=new_id))
    else:
        return render_template("add_card.html")


@app.route("/remove_card/<int:id>", methods=["GET", "POST"])
def remove_card(id):
    if request.method == "POST":
        dbh.remove_card(id)
        return redirect(url_for("welcome"))
    else:
        card = {}
        _, card["question"], card["answer"] = dbh.get_card_by_id(id)
        print(card)
        return render_template("remove_card.html", card=card)


@app.route("/api/card/")
def api_card_list():
    # List cannot be directly serialized for security reasons
    # The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a list.
    return jsonify(db)


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)