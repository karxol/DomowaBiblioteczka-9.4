from flask import Flask, jsonify , abort, make_response, request
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/books/", methods=["GET"])
def books_list():
    return jsonify(books.all())

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})

@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books.all()[-1]['id'] + 1,
        'author': request.json['author'],
        "year" : request.json['year'],
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    books.create(book)
    return jsonify({'book': book}), 201

@app.route("/api/v1/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', book['title']),
        'description': data.get('description', book['description']),
        'done': data.get('done', book['done'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

if __name__ == "__main__":
    app.run(debug=True)