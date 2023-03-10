from flask import Flask, request, jsonify, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

database_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "jopa6262"))
session = database_connection.session()

@app.route('/')
def preprocessing():
    return render_template("search.html")


@app.route('/search_by_name', methods=['POST', 'GET'])
def search():
    name = request.form['name']
    q = f'MATCH(:participant{{name:"{name}"}})-[:takes_part_in]->(id:event_id) return id'
    response = session.run(q).data()
    if response:
        return render_template('search.html', info=response)
    else:
        return render_template('search.html', info="No person with that name has been found")

if __name__ == "__main__":
    app.run(port="5050")