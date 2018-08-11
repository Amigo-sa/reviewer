from flask import Flask, jsonify, request
app = Flask(__name__)

existing_nodes = []

@app.route("/register", methods = ['POST'])
def register():
    a = request.get_json()
    if not a in existing_nodes:
        existing_nodes.append(a)
        print("New node registered: ",a)
    return '', 200

@app.route("/get_network_info", methods = ['GET'])
def get_network_info():
    return jsonify(existing_nodes), 200

app.run()