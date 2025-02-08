import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
BACKEND_URL = os.getenv('BACKEND_URL')


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship(
        "Author",
        backref=db.backref(
            "books",
            uselist=True,
        ),
    )
    title = db.Column(
        db.Text,
        nullable=False,
    )
    isbn10 = db.Column(
        db.String(32),
        unique=True,
    )
    isbn13 = db.Column(
        db.String(32),
        unique=True,
    )
    cover = db.Column(db.String(256))
    have_read = db.Column(
        db.Boolean,
        default=False,
    )
    is_awesome = db.Column(
        db.Boolean,
        default=True,
    )

    def __repr__(self):
        return f"<Book: {self.title}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "author": f"{BACKEND_URL}api/authors/{self.author.id}",
            "title": self.title,
            "isbn10": self.isbn10,
            "isbn13": self.isbn13,
            "cover": self.cover,
            "have_read": self.have_read,
            "is_awesome": self.is_awesome,
        }


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.String(256),
    )
    # There is a secret "books" property added by
    # the backref of the relationship.  Pretend
    # you can see it and you'll be fine.

    def __repr__(self):
        return f"<Author: {self.name}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "books": [f"{BACKEND_URL}api/books/{book.id}" for book in self.books], 
        }
