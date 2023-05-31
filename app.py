
from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


#MongoDB user permissions chaged to modify all databases
uri = "mongodb+srv://Brain3DVizMember:9GyKqp4b9blclzqJ@tinyurl-experimental.cuym0r0.mongodb.net/?retryWrites=true&w=majority"

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
    input_value = data.get('input')

    # Process the input value as needed
    # Perform any necessary calculations or operations

    # Create a response JSON with the output
    output_value = "Processed: " + input_value
    response = {'output': output_value}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug = True)
