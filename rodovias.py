import heapq
from csv import *

estradas = {1:{'status':None,'neighbor':{2:3,5:2 },'cost':10000,'from':None,'latitude':1, 'longitude':2},
            2:{'status':None,'neighbor':{1:3,3:2,5:0},'cost':10000,'from':None, 'latitude':4, 'longitude':5},
            3:{'status':None,'ne ighbor':{2:2,4:4,5:6},'cost':10000,'from':None, 'latitude':6, 'longitude':7},
            4:{'status':None,'neighbor':{3:4,5:4},'cost':10000,'from':None, 'latitude':12, 'longitude':3},
            5:{'status':None,'neighbor':{1:2,2:0,3:6,4:4},'cost':10000,'from':None, 'latitude':3, 'longitude':9}}

def render_csv(csv_file):
   roads_list = []
   with open(csv_file, 'rb') as f:
      r = reader(f)
      for row in r:
         roads_list.append(row)
   del roads_list[0]
   for road in roads_list:
      if road[1] == '1':
         road[4] = 0
      for pos, i in enumerate(road):
         road[pos] = float(i)
   return roads_list


def node_test(v_1,graph):
   for node in graph:
      if graph[node]['latitude'] == v_1['lat'] and graph[node]['longitude'] == v_1['lon']:
         return node
   return False

#cria dicionario onde cada chave e uma estrada, e o value sao todos seus pontos
def create_dict(roads_list):
   roads_dict = {}
   #constroi dicionario de estradas
   for i in range(1,635):
      roads_dict[i] = []
      list_aux = []
      for road in roads_list:
         if road[0] == i:
            list_aux.append(road)
      for road in list_aux:
         new_latlng = {'lat': road[3],'lon':road[2], 'cost': road[4]}
         roads_dict[i].append(new_latlng)
   return roads_dict

#cria o grafo onde cada no e o inicio e o final de uma estrada.
def create_graph(roads_dict):
   #constroi vertices
   graph = {}
   count_node = 1
   for road in roads_dict:
      distance = 0
      v_1 = roads_dict[road][0]
      v_2 = roads_dict[road][-1]
      for i in roads_dict[road]:
         distance = distance + i['cost']
      ans = node_test(v_1,graph)
      ans2 = node_test(v_2,graph)
      if ans == False:
         if ans2 == False:
            graph[count_node] = {'roads':[road],'status':None,'neighbor':{count_node+1:distance},'cost':'inf','from':None,'latitude':v_1['lat'] , 'longitude':v_1['lon']}
            graph[count_node+1] = {'roads':[road],'status':None,'neighbor':{count_node:distance},'cost':'inf','from':None,'latitude':v_2['lat'] , 'longitude':v_2['lon']}
            count_node += 2
         else:
            graph[count_node] = {'roads':[road],'status':None,'neighbor':{ans2:distance},'cost':'inf','from':None,'latitude':v_1['lat'] , 'longitude':v_1['lon']}
            new_neighbor = {count_node:distance}
            graph[ans2]['neighbor'].update(new_neighbor)
            graph[ans2]['roads'].append(road)
            count_node +=1
      elif ans2 == False:
            graph[count_node] = {'roads':[road],'status':None,'neighbor':{ans:distance},'cost':'inf','from':None,'latitude':v_2['lat'] , 'longitude':v_2['lon']}
            new_neighbor = {count_node:distance}
            graph[ans]['neighbor'].update(new_neighbor)
            graph[ans]['roads'].append(road)
            count_node +=1
      else:
         new_neighbor = {ans:distance}
         new_neighbor2 = {ans2:distance}
         graph[ans]['neighbor'].update(new_neighbor2)
         graph[ans]['roads'].append(road)
         graph[ans2]['neighbor'].update(new_neighbor)
         graph[ans2]['roads'].append(road)
   return graph

def min_value(graph):
   x = [10000,None]
   for node in graph:
      if graph[node]['status'] == 'visited':
         if graph[node]['cost'] < x[0]:
            x = [graph[node]['cost'],node]
   return x[1]


def Dijkstra(graph,start,finish):
   graph[start]['cost'] = 0
   list_nodes = []
   current = start
   while graph[finish]['status'] != 'fixed':

      graph[current]['status'] = 'fixed'
      for neighbor in graph[current]['neighbor']:
         neighbor_cost =  graph[neighbor]['cost']
         new_cost = graph[current]['neighbor'][neighbor]+graph[current]['cost']
         if new_cost < neighbor_cost:
            graph[neighbor]['cost'] = new_cost
            graph[neighbor]['from'] = current
            graph[neighbor]['status'] = 'visited'
      current = min_value(graph)
   return graph

def caminho(graph,start,finish,l):
   a = graph[finish]['from']
   l.append(a)
   if a != start:
      caminho(graph, start, a,l)
   return l

def shortest_path(graph,start,finish):
   if start == finish:
      return {'nodes': start, 'roads': []}
   nodes_list = [finish]
   road_list = []
   path = Dijkstra(graph,start,finish)
   ans = caminho(path,start,finish,nodes_list)
   path_list = nodes_list[::-1]
   for i, node in enumerate(path_list[:-1]):
      for road in graph[node]['roads']:
         next = path_list[i+1]
         if road in graph[next]['roads']:
            road_list.append(road)
            break
   return {'nodes': path_list, 'roads': road_list}

lista = render_csv('estradas_distancias.csv')
dit = create_dict(lista)
graph = create_graph(dit)
#print shortest_path(estradas,1,2)
# print teste

   




