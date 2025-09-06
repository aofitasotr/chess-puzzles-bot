from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.BigInteger, unique=True, nullable=False)
    registration_time = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_active = db.Column(db.DateTime)
    daily_puzzle_time = db.Column(db.DateTime)

    user_stat = db.relationship('UserStat', back_populates='user', uselist=False)
    puzzle_stats = db.relationship('UserPuzzleStat', back_populates='user')

class Puzzle(db.Model):
    __tablename__ = 'puzzle'

    puzzle_id = db.Column(db.Integer, primary_key=True)
    fen = db.Column(db.String, nullable=False)
    moves = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    tag = db.Column(db.String)

    puzzle_stats = db.relationship('UserPuzzleStat', back_populates='puzzle')

class UserStat(db.Model):
    __tablename__ = 'user_stat'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    puzzles_count = db.Column(db.Integer, default=0)
    attempts_count = db.Column(db.Integer, default=0)
    solutions_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='user_stat')

class UserPuzzleStat(db.Model):
    __tablename__ = 'user_puzzle_stat'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.puzzle_id'), primary_key=True)

    solved = db.Column(db.Boolean, default=False)
    attempts_count = db.Column(db.Integer, default=0)
    first_attempt_date = db.Column(db.DateTime)
    last_attempt_date = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='puzzle_stats')
    puzzle = db.relationship('Puzzle', back_populates='puzzle_stats')
