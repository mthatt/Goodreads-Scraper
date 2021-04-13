from flask import Flask, redirect, url_for
from flask_pymongo import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, make_response
from flask import render_template
import os
import queryInterpreter
app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://dbUser242:123qwe4r@cluster0.2qwnu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('goodreads')
user_collection = pymongo.collection.Collection(db, 'goodreads_info')

@app.route('/book', methods=['POST'])
def post_book():
    _json = request.json
    _title = _json['title']
    _book_url = _json['book_url']
    _author_url = _json['author_url']
    _author = _json['author']
    _rating = _json['rating']
    _rating_count = _json['rating_count']
    _review_count = _json['review_count']
    _image_url = _json['image_url']

    if _title and _book_url and _author_url and _author and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
        id = db.goodreads_info.insert_one({'title':_title, 'book_url':_book_url, 'author_url':_author, 'author':_author,
                                             'rating':_rating, 'rating_count':_rating_count, 'review_count':_review_count,
                                             'image_url':_image_url})
        resp = jsonify("Book updated successfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()

@app.route('/books', methods=['POST'])
def post_books():

    _json = request.json
    for currentBook in _json:
        _title = currentBook['title']
        _book_url = currentBook['book_url']
        _author_url = currentBook['author_url']
        _author = currentBook['author']
        _rating = currentBook['rating']
        _rating_count = currentBook['rating_count']
        _review_count = currentBook['review_count']
        _image_url = currentBook['image_url']

        if _title and _book_url and _author_url and _author and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
            id = db.goodreads_info.insert_one({'title':_title, 'book_url':_book_url, 'author_url':_author, 'author':_author,
                                           'rating':_rating, 'rating_count':_rating_count, 'review_count':_review_count,
                                           'image_url':_image_url})
            resp = jsonify("Book updated successfully")

            resp.status_code = 200
        else:
            return not_found()

    return resp

@app.route('/author', methods=['POST'])
def post_author():
    _json = request.json
    _name = _json['name']
    _author_url = _json['author_url']
    _rating = _json['rating']
    _rating_count = _json['rating_count']
    _review_count = _json['review_count']
    _image_url = _json['image_url']

    if _name and _author_url and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
        id = db.goodreads_info.insert_one({'name':_name, 'author_url':_author_url, 'rating':_rating, 'rating_count':_rating_count,
                                       'review_count':_review_count, 'image_url':_image_url,})
        resp = jsonify("Author updated successfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()

@app.route('/authors', methods=['POST'])
def post_authors():
    _json = request.json
    for currentAuthor in _json:
        _name = currentAuthor['name']
        _author_url = currentAuthor['author_url']
        _rating = currentAuthor['rating']
        _rating_count = currentAuthor['rating_count']
        _review_count = currentAuthor['review_count']
        _image_url = currentAuthor['image_url']

        if _name and _author_url and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
            id = db.goodreads_info.insert_one({'name':_name, 'author_url':_author_url, 'rating':_rating, 'rating_count':_rating_count,
                                           'review_count':_review_count, 'image_url':_image_url,})
            resp = jsonify("Authors updated successfully")

            resp.status_code = 200

        else:
            return not_found()
    return resp

@app.route('/book', methods = ['GET'])
def book():
    id = request.args.get('id')
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested book \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    resp = dumps(book)
    return resp

@app.route('/author', methods = ['GET'])
def author():
    id = request.args.get('id')
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    author = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if author is None:
        message = {
            'status': 404,
            'message': 'The requested author\'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    resp = dumps(author)
    return resp

@app.route('/search', methods = ['GET'])
def search():
    query = request.args.get('q')
    searchInfo = queryInterpreter.QueryInterpreter(query)

    if searchInfo.elements['field'] is None or (searchInfo.elements['search_term'] is None and searchInfo.elements['exact_search_term'] is None) and searchInfo.elements['operator'] is not ">" and searchInfo.elements['operator'] is not "<":
        message = {
            'status': 404,
            'message': 'Must provide a search field and term'}
        resp = jsonify(message)
        return resp

    if searchInfo.elements['operator'] is None:
        if searchInfo.elements['exact_search_term'] is not None:
            resp = db.goodreads_info.find({searchInfo.elements['field']: searchInfo.elements['exact_search_term']})
        else:
            resp = db.goodreads_info.find({searchInfo.elements['field']: {'$regex': searchInfo.elements['search_term']}})

    elif searchInfo.elements['operator'] is "AND":
        if searchInfo.elements['exact_search_term'] is not None:
            if searchInfo.elements['second_exact_search_term'] is not None:
                resp = db.goodreads_info.find( {searchInfo.elements['field']: searchInfo.elements['exact_search_term'],
                                            searchInfo.elements['second_field']: searchInfo.elements['second_exact_search_term']} )
            else:
                resp = db.goodreads_info.find( {searchInfo.elements['field']: searchInfo.elements['exact_search_term'],
                                                searchInfo.elements['second_field']: {'$regex': searchInfo.elements['second_search_term']}} )
        else:
            if searchInfo.elements['second_exact_search_term'] is not None:
                resp = db.goodreads_info.find( {searchInfo.elements['field']: {'$regex': searchInfo.elements['search_term']},
                                                searchInfo.elements['second_field']: searchInfo.elements['second_exact_search_term']} )
            else:
                resp = db.goodreads_info.find( {searchInfo.elements['field']: {'$regex': searchInfo.elements['search_term']},
                                                searchInfo.elements['second_field']: {'$regex': searchInfo.elements['second_search_term']}} )

    elif searchInfo.elements['operator'] is "OR":
        if searchInfo.elements['exact_search_term'] is not None:
            if searchInfo.elements['second_exact_search_term'] is not None:
                resp = db.goodreads_info.find( {'$or': [ {searchInfo.elements['field']: searchInfo.elements['exact_search_term']},
                                                         {searchInfo.elements['second_field']: searchInfo.elements['second_exact_search_term']}]})
            else:
                resp = db.goodreads_info.find( {'$or': [  {searchInfo.elements['field']: searchInfo.elements['exact_search_term']},
                                                          {searchInfo.elements['second_field']: {'$regex': searchInfo.elements['second_search_term']}}]})
        else:
            if searchInfo.elements['second_exact_search_term'] is not None:
                resp = db.goodreads_info.find( {'$or': [  {searchInfo.elements['field']: {'$regex': searchInfo.elements['search_term']}},
                                                          {searchInfo.elements['second_field']: searchInfo.elements['second_exact_search_term']}]})
            else:
                resp = db.goodreads_info.find( {'$or': [  {searchInfo.elements['field']: {'$regex': searchInfo.elements['search_term']}},
                                                           {searchInfo.elements['second_field']: {'$regex': searchInfo.elements['second_search_term']}}]})

    elif searchInfo.elements['operator'] is ">":
        resp = db.goodreads_info.find( {searchInfo.elements['field']: { '$gt': searchInfo.elements['second_search_term']}})

    elif searchInfo.elements['operator'] is "<":
        resp = db.goodreads_info.find( {searchInfo.elements['field']: { '$lt': searchInfo.elements['second_search_term']}})


    return dumps(resp)


@app.route('/author', methods=['PUT'])
def put_author():
    id = request.args.get('id')
    toUpdate = request.json
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested author \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.update({'_id' : ObjectId(id)},
                         {'$set' : {list(toUpdate.keys())[0] : list(toUpdate.values())[0] }})
    resp = jsonify("Author updated successfully")

    resp.status_code = 200

    return resp

@app.route('/book', methods=['PUT'])
def put_book():
    id = request.args.get('id')
    toUpdate = request.json
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested book \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.update({'_id' : ObjectId(id)},
                             {'$set': {list(toUpdate.keys())[0] : list(toUpdate.values())[0] }})
    resp = jsonify("Book updated successfully")

    resp.status_code = 200

    return resp

@app.route('/book', methods=['DELETE'])
def delete_book():
    id = request.args.get('id')
    toDelete = request.json
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested book \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.delete_one({'id':ObjectId(id)})
    resp = jsonify("Book deleted successfully")

    resp.status_code = 200

    return resp

@app.route('/author', methods=['DELETE'])
def delete_author():
    id = request.args.get('id')
    toDelete = request.json
    if len(id) != 24:
        message = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested author \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.delete_one({'id':ObjectId(id)})
    resp = jsonify("Author deleted successfully")

    resp.status_code = 200

    return resp

@app.errorhandler(404)
def not_found(error=None):
    messsage = {
        'status': 404,
        'message:': 'Request not found' + request.url
    }
    resp = jsonify(messsage)
    resp.status_code = 404
    return resp

@app.route("/postanauthor")
def postanauthor():
    return render_template("post_author.html")

@app.route("/postanauthor/create", methods=["POST"])
def postanauthor_create():


    _json = request.form
    _name = _json['name']
    _author_url = _json['author_url']
    _rating = _json['rating']
    _rating_count = _json['rating_count']
    _review_count = _json['review_count']
    _image_url = _json['image_url']

    if _name and _author_url and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
        id = db.goodreads_info.insert_one({'name':_name, 'author_url':_author_url, 'rating':_rating, 'rating_count':_rating_count,
                                           'review_count':_review_count, 'image_url':_image_url,})

    else:
        return not_found()


    return render_template("success.html")


@app.route("/postabook")
def postabook():
    return render_template("post_book.html")



@app.route("/postabook/create", methods=["POST"])
def postabook_create():
    print("X")

    _json = request.form
    _title = _json['title']
    _book_url = _json['book_url']
    _author_url = _json['author_url']
    _author = _json['author']
    _rating = _json['rating']
    _rating_count = _json['rating_count']
    _review_count = _json['review_count']
    _image_url = _json['image_url']

    if _title and _book_url and _author_url and _author and _rating and _rating_count and _review_count and _image_url and request.method == 'POST':
        id = db.goodreads_info.insert_one({'title':_title, 'book_url':_book_url, 'author_url':_author, 'author':_author,
                                           'rating':_rating, 'rating_count':_rating_count, 'review_count':_review_count,
                                           'image_url':_image_url})
    else:
        return not_found()
    return render_template("success.html")

@app.route("/updateauthor")
def update_author():
    return render_template("updateauthor.html")

@app.route("/updateauthor/create", methods=["PUT"])
def updateauthor_create():
    update = request.get_json()
    print(update)
    print(update['id'])
    id = update['id']

    id = update['id']
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    print(book)
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested author \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.update({'_id' : ObjectId(id)},
                             {'$set' : {update['key'] : update['value'] }})
    resp = jsonify("Author updated successfully")

    resp.status_code = 200

    return render_template("success.html")

@app.route("/updatebook")
def update_book():
    return render_template("updatebook.html")

@app.route("/updatebook/create", methods=["PUT"])
def updatebook_create():
    update = request.get_json()
    print(update)
    print(update['id'])
    id = update['id']
    if len(id) != 24:
        messsage = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(messsage)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested book \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.update({'_id' : ObjectId(id)},
                             {'$set' : {update['key'] : update['value'] }})
    resp = jsonify("Book updated successfully")

    resp.status_code = 200

    return render_template("success.html")

@app.route("/getbook")
def get_book_site():
    return render_template("getbook.html")

@app.route("/getbook/create", methods=["GET"])
def get_book_site_create():
    print("DFGS")
    update = request.args
    print(update['id'])
    id = update['id']
    if len(id) != 24:
        message = {
            'status': 404,
            'message': 'The requested ID must be a 24 character hex'
        }
        error = message['message']
        resp = jsonify(message)
        resp.status_code = 404
        return render_template("failure.html", error=error)
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    print(book)
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested book \'s ID was not found'}
        error = message['message']
        resp = jsonify(message)
        resp.status_code = 404
        return render_template("failure.html", error=error)
    resp = dumps(book)
    return render_template("showbook.html", book=book)

@app.route("/showbook/<book>")
def show_book(book):
    print(dumps(book))
    return render_template("showbook.html", book=book)

@app.route("/getauthor")
def get_author_site():
    return render_template("getauthor.html")

@app.route("/getauthor/create", methods=["GET"])
def get_author_site_create():
    print("DFGS")
    update = request.args
    print(update['id'])
    id = update['id']
    if len(id) != 24:
        message = {
            'status': 404,
            'message': 'The requested ID must be a 24 character hex'}
        error = message['message']
        resp = jsonify(message)
        resp.status_code = 404
        return render_template("failure.html", error=error)
    author = db.goodreads_info.find_one({'_id':ObjectId(id)})
    print(author)
    if author is None:
        message = {
            'status': 404,
            'message': 'The requested author\'s \'s ID was not found'}
        error = message['message']
        resp = jsonify(message)
        resp.status_code = 404
        return render_template("failure.html", error=error)
    resp = dumps(author)
    return render_template("showauthor.html", author=author)

@app.route("/deleteauthor")
def delete_author_site():
    return render_template("deleteauthor.html")
@app.route("/deleteauthor/create", methods=["DELETE"])
def delete_author_site_delete():
    update = request.get_json()
    print("SDFG")
    print(update['id'])
    id = update['id']
    if len(id) != 24:
        message = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    print(book)
    if book is None:
        print("found")
        message = {
            'status': 404,
            'message': 'The requested author\'s \'s ID was not found'}
        error = message['message']
        print(error)
        resp = jsonify(message)
        resp.status_code = 404
        return render_template("failure.html", error=error)
    db.goodreads_info.delete_one({'_id':ObjectId(id)})
    resp = jsonify("Author deleted successfully")

    resp.status_code = 200

    return render_template("success.html")

@app.route("/deletebook")
def delete_book_site():
    return render_template("deletebook.html")
@app.route("/deletebook/create", methods=["DELETE"])
def delete_book_site_delete():
    update = request.get_json()
    print(update)
    print(update['id'])
    id = update['id']
    if len(id) != 24:
        message = {
            'status': 404,
            'message:': 'The requested ID must be a 24 character hex'
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    book = db.goodreads_info.find_one({'_id':ObjectId(id)})
    if book is None:
        message = {
            'status': 404,
            'message': 'The requested author \'s ID was not found'}
        resp = jsonify(message)
        resp.status_code = 404
        return resp
    db.goodreads_info.delete_one({'_id':ObjectId(id)})
    resp = jsonify("Book deleted successfully")

    resp.status_code = 200

    return render_template("success.html")

@app.route("/showauthor/<author>")
def show_author(author):
    print(dumps(book))
    return render_template("showauthor.html", author=author)

@app.route("/success")
def success():
    print("S")
    return render_template("success.html")

@app.route("/deletesuccess")
def delete_success():
    print("S")
    return render_template("deletesuccess.html")

@app.route("/failure/<error>")
def failure():
    print("S")
    return render_template("failure.html", error=error)

@app.route("/failure")
def failure_E():
    print("S")
    return render_template("failure.html", error="The requested author\'s \'s ID was not found")

if __name__ == "__main__":
    app.run(debug=True)
