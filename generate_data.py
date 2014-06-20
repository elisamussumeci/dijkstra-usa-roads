import rodovias
import json

def generate_data(csv):
	roads_list = rodovias.render_csv(csv)
	roads_dict = rodovias.create_dict(roads_list)
	graph = rodovias.create_graph(roads_dict)
	return json.dumps(graph,indent = 4), json.dumps(roads_dict, indent = 4)

data_nodes,data = generate_data('estradas_distancias.csv')

a = open('static/js/data_nodes.js', 'w')
a.write('data_nodes =' + data_nodes)
a.close()
b = open('static/js/data.js', 'w')
b.write('data =' + data)
b.close()
