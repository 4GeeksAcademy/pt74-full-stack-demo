import os
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

db = SQLAlchemy()
BACKEND_URL = os.getenv('BACKEND_URL')


book_to_author = db.Table(
    "book_to_author",
    db.metadata,
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey('book.id', ondelete="CASCADE")
    ),
    db.Column(
        "author_id",
        db.Integer,
        db.ForeignKey('author.id', ondelete="CASCADE")
    ),
)

user_to_book = db.Table(
    "user_to_book",
    db.metadata,
    db.Column(
        "use_id",
        db.Integer,
        db.ForeignKey('user.id', ondelete="CASCADE")
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey('book.id', ondelete="CASCADE")
    ),
)

user_to_author = db.Table(
    "user_to_author",
    db.metadata,
    db.Column(
        "use_id",
        db.Integer,
        db.ForeignKey('user.id', ondelete="CASCADE")
    ),
    db.Column(
        "author_id",
        db.Integer,
        db.ForeignKey('author.id', ondelete="CASCADE")
    ),
)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.String(256),
        unique=True,
        nullable=False,
    )
    _password = db.Column(
        db.String(256),
        nullable=False,
    )

    fav_books = db.relationship("Book", secondary=user_to_book, uselist=True)
    fav_authors = db.relationship("Author", secondary=user_to_author, uselist=True)

    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f"<User: {self.email}>"
    
    # def url(self):
    #     return f"{BACKEND_URL}api/users/{self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fav_authors": [author.url() for author in self.fav_authors],
            "fav_books": [book.url() for book in self.fav_books],
        }


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    authors = db.relationship(
        "Author",
        back_populates="books",
        secondary=book_to_author,
        passive_deletes=True,
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
    
    def url(self):
        return f"{BACKEND_URL}api/books/{self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            # "author": f"{BACKEND_URL}api/authors/{self.author.id}",
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

    books = db.relationship(
        "Book",
        back_populates="authors",
        secondary=book_to_author,
        cascade="all, delete",
    )

    def __repr__(self):
        return f"<Author: {self.name}>"
    
    def url(self):
        return f"{BACKEND_URL}api/authors/{self.id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "books": [f"{BACKEND_URL}api/books/{book.id}" for book in self.books],
        }
