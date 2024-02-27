#!/usr/bin/python3
""" City view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ retrieves the list of all reviews object of a place """
    ret_place = storage.get(Place, place_id)
    if ret_place is None:
        abort(404)
    reviews = []
    for review in ret_place.reviews:
        review_dic = to_dict(review)
        reviews.append(review_dic)
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ retreives a review with the review_id """
    ret_review = storage.get(Review, review_id)
    if ret_review is None:
        abort(404)
    return jsonify(to_dict(ret_review))


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review with the given review_id """
    ret_review = storage.get(Review, review_id)
    if ret_review is None:
        abort(404)
    storage.delete(ret_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def add_new_review(place_id):
    """ adds a new review to the given place_id """
    ret_place = storage.get(Place, place_id)
    if ret_place is None:
        abort(404)
    add_review = request.get_json()
    user = storage.get(User, add_review['user_id'])
    if not add_review:
        abort(400, "Not a JSON")
    elif not user:
        abort(404)
    elif 'text' not in add_review:
        abort(400, "Missing text")
    else:
        new_review = Review(**add_review)
        setattr(new_review, "place_id", place_id)
        storage.new(new_review)
        storage.save()
        return jsonify(to_dict(new_review)), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates a rewiew value of a given review id """
    ret_review = storage.get(Review, review_id)
    if ret_review is None:
        abort(404)
    put_data = request.get_json()
    if not put_data:
        abort(400, "Not a JSON")
    put_data.pop('id', None)
    put_data.pop('created_at', None)
    put_data.pop('updated_at', None)
    put_data.pop('state_id', None)

    for key, value in put_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(ret_review, key, value)
    storage.save()
    return jsonify(to_dict(ret_review)), 200
