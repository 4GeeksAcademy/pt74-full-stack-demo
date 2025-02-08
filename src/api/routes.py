"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Book, Author
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route("/authors", methods=["GET"])
def get_authors():
    authors = Author.query.all()
    return jsonify({
        "count": len(authors),
        "authors": [author.serialize() for author in authors]
    })


@api.route("/authors/<int:id>", methods=["GET"])
def get_author(id: int):
    author = Author.query.filter_by(id=id).first()
    return jsonify(author.serialize())


@api.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify({
        "count": len(books),
        "books": [book.serialize() for book in books]
    })


@api.route("/books/<int:id>", methods=["GET"])
def get_book(id: int):
    book = Book.query.filter_by(id=id).first()
    return jsonify(book.serialize())
