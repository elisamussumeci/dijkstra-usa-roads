from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response, jsonify
import json
import rodovias
import copy


app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')


lista = rodovias.render_csv('estradas_distancias.csv')
dit = rodovias.create_dict(lista)
graph = rodovias.create_graph(dit)

@app.route("/shortest/<int:a>/<int:b>")
def shortest(a,b):
	graph_copy = copy.deepcopy(graph)
	path = rodovias.shortest_path(graph_copy,a,b)
	return jsonify(path)


if __name__ == "__main__":
    app.run(port=8000, debug=True)