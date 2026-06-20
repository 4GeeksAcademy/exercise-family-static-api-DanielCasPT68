"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)

jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})

jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})

jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})


@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(jackson_family.get_all_members()), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)

    if member is None:
        return jsonify({"error": "Member not found"}), 404

    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def add_member():
    request_body = request.json

    new_member = jackson_family.add_member(request_body)

    return jsonify(new_member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    was_deleted = jackson_family.delete_member(member_id)

    if was_deleted:
        return jsonify({"done": True}), 200

    return jsonify({"error": "Member not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)