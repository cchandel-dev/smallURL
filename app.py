
from flask import Flask, render_template, request, jsonify, session
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi        
import hashlib
import base64


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
    cl.insert_one({'long_link': 'John', 'short_link': ''})
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    link = data.get('input')
    if link:
        try:
            response = requests.head(link)
            if response.status_code == requests.codes.ok:
                response = encode(link) #encode called from here
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


def encode(link):
    # String to search for

    # Query the collection to check if the string exists
    result = cl.find_one({"long_link": link})

    if result is not None:
        short_link = 'from db: ' + result["short_link"]
        return short_link
    else:
        short_link = generate_unique_string(link)
        cl.insert_one({'long_link': link, 'short_link': short_link})
        return 'from encoder: ' + short_link



def generate_unique_string(input_string):
    # Hash the input string using SHA-256
    hashed = hashlib.sha256(input_string.encode()).digest()

    # Take the first 6 bytes of the hash and encode it in base64
    encoded = base64.b64encode(hashed[:6]).decode()

    # Take the first 7 characters of the encoded string
    unique_string = encoded[:7]

    return unique_string


if __name__ == '__main__':
    app.run(debug = True)
