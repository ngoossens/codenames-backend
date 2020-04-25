from random import choice, shuffle

from sqlalchemy import func

from . import db, ma
from ..methods.utility import generate_id
from .cards import Card
from .words import Word

CARDS_PER_GAME = 25
GAME_ID_CHARACTERS = 6


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.String(20), primary_key=True)
    ready = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    complete = db.Column(db.Boolean, default=False)

    cards = db.relationship("Card", backref="game", cascade="all, delete")

    def __init__(self):
        game_id = None
        while game_id is None or Game.query.get(game_id) is not None:
            game_id = generate_id(GAME_ID_CHARACTERS)

        self.id = game_id

        teams = (["BLUE"] * 8) + (["RED"] * 8) + (["NEUTRAL"] * 7) + ["DEATH"]
        teams += [choice(["BLUE", "RED"])]
        shuffle(teams)

        words = Word.query.order_by(func.random()).limit(CARDS_PER_GAME)
        for word, team in zip(words, teams):
            card = Card(word=word.word, team=team, game=self)
            db.session.add(card)


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game


game_schema = GameSchema()
games_schema = GameSchema(many=True)
