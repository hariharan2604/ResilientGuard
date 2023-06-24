import socket

from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Set up MongoDB Atlas connection
client = MongoClient(
    'mongodb+srv://hariharan2604:hariHARAN-2604@atlastest.a6oo0uf.mongodb.net/?retryWrites=true&w=majority')
print('db connected')
db = client['dbusers']
collection = db['users']


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')

    print(email)
    print(password)

    # Perform authentication logic here
    user = collection.find_one({'email': email, 'password': password})
    print(user)
    if user:
        return render_template('index.html')  # Redirect to index page
    else:
        return render_template('login.html', error='Invalid email or password.')


@app.route('/form1', methods=['GET'])
def process_form():
    disaster = "Natural"
    disastertype = request.args.get('dtype')
    subgroup = request.args.get('sgroup')

    print(disaster + " " + disastertype + " " + subgroup)

    c = socket.socket()
    print('client socket is created')

    c.connect(('localhost', 10000))
    print('connected')

    data = str(disaster) + "/" + str(disastertype) + "/" + str(subgroup)

    c.send(str(data).encode())

    data = c.recv(1024).decode()

    a = data.split("/")

    manpower = "Available manpower: " + a[0]
    req_manpower = "Required manpower(As per Prediction): " + a[1]
    remain = "Remaining manpower in reserve: " + a[2]

    print(manpower)
    print(req_manpower)
    print(remain)

    c.close()
    # return "hello"
    return render_template("alloc.html", available=manpower, alloted=req_manpower, remain=remain)


if __name__ == "__main__":
    app.run(debug=True)
