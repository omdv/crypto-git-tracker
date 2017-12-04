# project/api/models.py


from project import db


class Commit(db.Model):
    __tablename__ = "commits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, author, message, type, date):
        self.author = author
        self.message = message
        self.type = type
        self.date = date
