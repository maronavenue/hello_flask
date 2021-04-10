#import json

seed_data = [
    { "question": "Good morning", "answer": "お早うございます" },
    { "question": "Nice to meet you", "answer": "始めまして" },
    { "question": "Good evening", "answer": "こんにちは" },
    { "question": "I am home", "answer": "只今; 唯今" },
    { "question": "Good night", "answer": "おやすみなさい" },
    { "question": "Welcome", "answer": "いらっしゃいませ" }
]


def load_db():
    return seed_data


def save_db():
    pass
#def load_db():
#    with open("flashcards_db.json", encoding="utf8") as f:
#        return json.load(f)


#def save_db():
#    with open("flashcards_db.json", "w") as f:
#        json.dump(db, f)


db = load_db()