from flask import Flask, escape, request
from flask import jsonify

import models

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/humanoids/')
def humanoids():
    if request.method == 'POST':
        data = request.json

        humanoid = models.Humanoid(data=data)
        humanoid.save()
    
    humanoids_list = models.Humanoid.get_list()
    return jsonify(humanoids_list)

@app.route('/humanoids/<humanoid_id>', methods=['GET', 'PUT', 'DELETE'])
def humanoid(humanoid_id):
    if request.method == 'GET':
        humanoid = models.Humanoid.get_by_pk(humanoid_id)
        return jsonify(humanoid.to_dict())
