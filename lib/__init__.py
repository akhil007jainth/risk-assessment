from flask import Flask
from mongoengine import connect

app = Flask(__name__)

# Configure MongoEngine connection
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'localhost',
    'port': 27017
}

# Connect to MongoDB
connect(
    db=app.config['MONGODB_SETTINGS']['db'],
    host=app.config['MONGODB_SETTINGS']['host'],
    port=app.config['MONGODB_SETTINGS']['port']
)

