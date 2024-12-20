from flask import Blueprint, jsonify, request
import secrets
from functools import wraps

library_blueprint = Blueprint("library", __name__)
secret_token = "672c4ec107adbee58f0ef6c2571ed9854688d7137d06e513"

# In-memory storage
from models import books, members, Book, Member

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token or token != secret_token:
            return jsonify({"message": "Token is missing or invalid"}), 403
        return f(*args, **kwargs)
    return decorated

# Books CRUD
@library_blueprint.route("/books", methods=["GET"])
def get_books():
    return jsonify([book.__dict__ for book in books])

@library_blueprint.route("/books", methods=["POST"])
@token_required
def add_book():
    data = request.json
    new_book = Book(
        book_id=len(books) + 1,
        title=data.get("title"),
        author=data.get("author"),
        year=data.get("year"),
    )
    books.append(new_book)
    return jsonify(new_book.__dict__), 201

@library_blueprint.route("/books/<int:book_id>", methods=["PUT"])
@token_required
def update_book(book_id):
    data = request.json
    book = next((b for b in books if b.book_id == book_id), None)
    if book:
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.year = data.get("year", book.year)
        return jsonify(book.__dict__)
    return jsonify({"error": "Book not found"}), 404

@library_blueprint.route("/books/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book(book_id):
    global books
    books = [b for b in books if b.book_id != book_id]
    return jsonify({"message": "Book deleted"})

# Members CRUD
@library_blueprint.route("/members", methods=["GET"])
def get_members():
    return jsonify([member.__dict__ for member in members])

@library_blueprint.route("/members", methods=["POST"])
@token_required
def add_member():
    data = request.json
    new_member = Member(
        member_id=len(members) + 1,
        name=data.get("name"),
        email=data.get("email"),
    )
    members.append(new_member)
    return jsonify(new_member.__dict__), 201

@library_blueprint.route("/members/<int:member_id>", methods=["PUT"])
@token_required
def update_member(member_id):
    data = request.json
    member = next((m for m in members if m.member_id == member_id), None)
    if member:
        member.name = data.get("name", member.name)
        member.email = data.get("email", member.email)
        return jsonify(member.__dict__)
    return jsonify({"error": "Member not found"}), 404

@library_blueprint.route("/members/<int:member_id>", methods=["DELETE"])
@token_required
def delete_member(member_id):
    global members
    members = [m for m in members if m.member_id != member_id]
    return jsonify({"message": "Member deleted"})

# Search functionality
@library_blueprint.route("/books/search", methods=["GET"])
def search_books():
    query = request.args.get("q", "").lower()
    results = [
        book.__dict__
        for book in books
        if query in book.title.lower() or query in book.author.lower()
    ]
    return jsonify(results)

# Pagination
@library_blueprint.route("/books/paginated", methods=["GET"])
def get_paginated_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    start = (page - 1) * per_page
    end = start + per_page
    paginated_books = books[start:end]
    return jsonify([book.__dict__ for book in paginated_books])
