from bson import ObjectId
from flask import Flask, jsonify, request
from flask_bcrypt import generate_password_hash

from db import mongo, initialize_db

app = Flask(__name__)

# Configure the MongoDB URI
app.config['MONGO_URI'] = 'mongodb+srv://tenants:nKbkhQr4grmjpzPC@cluster0.hi2lkdm.mongodb.net/flask'

# Initialize PyMongo
initialize_db(app)


@app.route('/')
def index():
    data = mongo.db.users.find()
    data = list(data)
    for item in data:
        item['_id'] = str(item['_id'])

    return jsonify(data)


@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    if data:
        if 'password' in data:
            hashed_password = generate_password_hash(data['password']).decode('utf-8')
            data['password'] = hashed_password
        inserted = mongo.db.users.insert_one(data)
        return jsonify({'inserted_id': str(inserted.inserted_id)})
    else:
        return jsonify({'error': 'No data provided'}), 400


@app.route('/update/<id>', methods=['POST'])
def update(id):
    data = request.json
    if data:
        if 'password' in data:
            hashed_password = generate_password_hash(data['password']).decode('utf-8')
            data['password'] = hashed_password
        result = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': data})

        if result.modified_count > 0:
            return jsonify({'message': 'Record updated successfully'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    else:
        return jsonify({'error': 'No data provided'}), 400


@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    result = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'error': 'Record not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
