import copy

from flask import (Flask, render_template, abort, jsonify, request,
                    redirect, url_for)
# from model import db, save_db

app = Flask(__name__)
seed_db = [
    { "question": "Good morning", "answer": "お早うございます" },
    { "question": "Nice to meet you", "answer": "始めまして" },
    { "question": "Good evening", "answer": "こんにちは" },
    { "question": "I am home", "answer": "只今; 唯今" },
    { "question": "Good night", "answer": "おやすみなさい" },
    { "question": "Welcome", "answer": "いらっしゃいませ" }
]
flashcards_db = copy.deepcopy(seed_db)

@app.route("/")
def welcome():
    return render_template("welcome.html", cards=flashcards_db)


@app.route("/card/<int:index>")
def card_view(index):
    try:
        card = flashcards_db[index]
        return render_template("card.html", card=card, index=index, max_index=len(flashcards_db)-1)
    except IndexError:
        abort(404)


@app.route("/add_card/", methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        card = {
            "question": request.form["question"],
            "answer": request.form["answer"]
        }
        global flashcards_db
        flashcards_db.append(card)
        return redirect(url_for("card_view", index=len(flashcards_db)-1))
    else:
        return render_template("add_card.html")


@app.route("/remove_card/<int:index>", methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            global flashcards_db
            flashcards_db.pop(index)
            return redirect(url_for("welcome"))
        else:
            return render_template("remove_card.html", card=flashcards_db[index])
    except IndexError:
        abort(404)


@app.route("/api/card/")
def api_card_list():
    # List cannot be directly serialized for security reasons
    # The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a list.
    return jsonify(flashcards_db)


@app.route("/api/card/<int:index>")
def api_card_detail(index):
    try:
        return flashcards_db[index]
    except IndexError:
        abort(404)
