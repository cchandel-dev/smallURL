
from flask import Flask, render_template, request, jsonify, session
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


#MongoDB user permissions chaged to modify all databases
uri = "mongodb+srv://Brain3DVizMember:9GyKqp4b9blclzqJ@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"
counter = 0
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['tinyURL-experimental'] #Select the database
cl = db['test'] #Select the collection name

app = Flask(__name__)

@app.route('/')
def index():
    # Store data in MongoDB
    cl.insert_one({'name': 'John', 'age': 25})
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    link = data.get('input')
    if link:
        try:
            response = requests.head(link)
            if response.status_code == requests.codes.ok:
                response = 'Link is valid' #encode called from here
            else:
                response = 'Link is not valid'
        except requests.exceptions.RequestException:
            response = 'Link is not valid'
    else:
        response = 'No link provided'

    # Process the input value as needed
    # Perform any necessary calculations or operations

    # Create a response JSON with the output
    response = {'output': response}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)
