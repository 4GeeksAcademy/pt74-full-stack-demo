"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Book, Author, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route("/login", methods=["POST"])
def login():
    """
    POST:
    {
        "email": str,
        "password": str
    }
    """
    body = request.get_json(force=True)

    user = User.query.filter_by(email=body.get("email")).first()

    if (
        not user or
        not user.check_password(body.get("password"))
    ):
        return jsonify(
            msg="Invalid email or password."
        ), 400

    return jsonify(
        token=create_access_token(
            identity=user
        )
    )


@api.route("/signup", methods=["POST"])
def signup():
    """
    POST:
    {
        "email": str,
        "password": str
    }

    Response:
    {
        "id": int,
        "email": str,
        "fav_authors": Author[],
	    "fav_books": Book[]
    }
    """
    body = request.get_json(force=True)

    user = User.query.filter_by(email=body.get("email")).first()

    if user:
        return jsonify(
            msg="User already exists with this email."
        ), 400
    
    user = User(**body)

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return jsonify(user.serialize())


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(
        identity=get_jwt_identity()
    )


@api.route("/users", methods=["GET"])
def read_users():
    users = User.query.all()
    return jsonify({
        "count": len(users),
        "authors": [user.serialize() for user in users],
    })


@api.route("/user/fav-book/<int:book_id>", methods=["PUT", "POST"])
@jwt_required()
def add_favorite_book(book_id: int):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return jsonify(
            msg=f"Book with ID {book_id} does not exist.",
        )
    
    current_user.fav_books.append(book)
    db.session.merge(current_user)
    db.session.commit()
    db.session.refresh(current_user)

    return jsonify(current_user.serialize())


@api.route("/authors", methods=["GET"])
def read_authors():
    authors = Author.query.all()
    return jsonify({
        "count": len(authors),
        "authors": [author.serialize() for author in authors],
    })


@api.route("/authors/<int:id>", methods=["GET"])
def read_author_by_id(id: int):
    author = Author.query.filter_by(id=id).first()
    return jsonify(author.serialize())


@api.route("/authors/<string:name>", methods=["POST"])
def create_author(name: str):
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()
    db.session.refresh(author)
    return jsonify(author.serialize())


@api.route("/books", methods=["GET"])
def read_books():
    # This endpoint lets you filter on the properties of
    # books that come in via url search paramaters.
    args = request.args
    books = Book.query.filter_by(**args).all()
    return jsonify({
        "count": len(books),
        "books": [book.serialize() for book in books],
    })


@api.route("/books/<int:id>", methods=["GET"])
def read_book(id: int):
    book = Book.query.filter_by(id=id).first()
    return jsonify(book.serialize())


@api.route("/books", methods=["POST"])
def create_book():
    """
    POST:
    {
        "title": str,
        "author_id?": int,
        "isbn10?": str,
        "isbn13?": str,
        "cover?": str,
        "have_read?": bool,
        "is_awesome?": bool,
    }
    """
    # We extract data from the request body that
    # is sent to our backend as JSON text.
    body = request.get_json(force=True)

    if "title" not in body.keys():
        return jsonify(msg="Books need titles"), 400
    
    if body.get("isbn10") or body.get("isbn13"):
        book = Book.query.filter_by(
            isbn10=body.get("isbn10"),
            isbn13=body.get("isbn13"),
        ).first()

        if book:
            return jsonify(msg="ISBN already in databse."), 400

    book = Book(**body)

    # We're relating two objects.
    if "author_id" in body.keys():
        author = Author.query.filter_by(id=body["author_id"]).first()
        book.author = author

    db.session.add(book)
    db.session.commit()
    db.session.refresh(book)
    return jsonify(book.serialize())
