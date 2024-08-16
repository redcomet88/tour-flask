from . import db

class Tour(db.Model):
    __tablename__ = 'tb_tour'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_en = db.Column(db.String(255))
    img = db.Column(db.String(255))
    score = db.Column(db.Float)
    comments = db.Column(db.Integer)
    comment_url = db.Column(db.String(255))
    rank_title = db.Column(db.String(255))
    ranks = db.Column(db.Integer)
    select_user = db.Column(db.String(255))
    select_comment = db.Column(db.Text)
    nation = db.Column(db.String(255))
    city = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    age = db.Column(db.Integer)
    intro = db.Column(db.String(255))
    addr = db.Column(db.String(100))
    idno = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    job = db.Column(db.String(10))
    roles = db.Column(db.String(50))
    deleted = db.Column(db.Integer)