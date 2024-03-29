from flask import Flask
from db import mongo, initialize_db

app = Flask(__name__)

# Configure the MongoDB URI
app.config['MONGO_URI'] = 'mongodb+srv://tenants:nKbkhQr4grmjpzPC@cluster0.hi2lkdm.mongodb.net/flask'

# Initialize PyMongo
initialize_db(app)


@app.route('/')
def index():
    data = mongo.db.users.find_one()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)