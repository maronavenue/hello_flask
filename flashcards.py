import copy
import os

from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for, current_app, send_from_directory,
                   Blueprint)
from flask_restplus import Api, Resource, fields
from model import DbStore


app = Flask(__name__)

with app.app_context():
    dbh = DbStore()
print("Inside the app!")

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, version="0.1.10", title="Nihongo flash cards API",
          description="A simple Rest API to serve related data")
app.register_blueprint(blueprint)

ns = api.namespace('flashcards', description="Operations related to flash cards")

flashcards = api.model('Hello', {
    "question": fields.String(required=True, description="Write the front size of the card (in your native language)."),
    "answer": fields.String(required=True, description="Write the corresponding Nihongo translation at the back of this same card.")
})

# parser = ns.parser()
# parser.add_argument("flashcard", type=list, required=True, help="Write the front size of the card (in your native language).", location="json")
# parser.add_argument("answer", type=str, required=True, help="Write the corresponding Nihongo translation at the back of this same card.", location="args")




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


@ns.route("/")
class Cards(Resource):

    def get(self):
        return jsonify(dbh.get_all_cards())


    @ns.expect(flashcards)
    def post(self):
        question = request.json["question"].strip()
        answer = request.json["answer"].strip()
        new_id = dbh.add_card(question, answer)
        new_card = dbh.get_card_by_id(new_id)
        resp = {}
        resp["id"], resp["question"], resp["answer"] = new_card
        return resp


@ns.route("/<int:id>")
@api.response(404, 'Flash card could not found.')
@api.response(200, 'Success')
class Card(Resource):

    def get(self, id):
        card = dbh.get_card_by_id(id)
        if not card:
            return None, 404
        resp = {}
        resp["id"], resp["question"], resp["answer"] = card
        return resp


    def delete(self, id):
        card = dbh.get_card_by_id(id)
        if not card:
            return None, 404
        dbh.remove_card(id)
        resp = { "message": "Successfully deleted flash card: {}".format(id) }
        return resp


@ns.route("/reset")
class CardReset(Resource):

    def post(self):
        dbh.reset_db_and_load_seed_data()
        resp = { "message": "Successfully reset data to original state!" }
        return resp