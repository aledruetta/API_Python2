from flask_login import UserMixin

from projeto.ext.db import db


class UserAuth(UserMixin, db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(255), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)

    def __repr__(self):
        return f"{self.id}: {self.email}"
