import networkx as nx
import sys;
#get folder containing the graph shapefiles
pathShape= raw_input("insert shapefile folder path:")
G=nx.read_shp(pathShape)

InitialGraph=G.to_undirected()

attributeLength=nx.get_edge_attributes(InitialGraph,'st_length')

#transform attribute length of the edge in time to travel it
for e,v,d in InitialGraph.edges_iter(data=True):
	InitialGraph.add_edge(e,v,time=(attributeLength[e,v]*51)/5594)

#initialize length function (length of shortest path will be calculated using dijkstra algorithm)
length=nx.all_pairs_dijkstra_path_length(InitialGraph,cutoff=None, weight='time')
GraphPath=InitialGraph
#add attribute totallength on each graph node and initialize it to 0
for n in GraphPath.nodes_iter():GraphPath.add_node(n,totalLength=0)
#get array containing the room names (nodes attribute)
shape=nx.get_node_attributes(GraphPath,'ShpName')
#start algorithm for every node
for node1,d in InitialGraph.nodes_iter(data=True):
	if ('ShpName' in d)==True:#check if the start node is a room then continue
		for node2 in length[node1]:
			try: 
				shapeTry=shape[node2]#check if the end node is a room
				totalLength=nx.get_node_attributes(GraphPath,'totalLength')#get array totallength
				try: totalDis=totalLength[node2]+length[node1][node2] #add total length
				except KeyError: totalDis=length[node1][node2]#add total length for the first time
				GraphPath.add_node(node2,totalLength=totalDis)#assign totalLength
			except KeyError: pass #the end node is not a room



#search minor total length, the result could be just a room 
MinDistanceNode=0
MinDistance=100000000000000
totalLength=nx.get_node_attributes(GraphPath,'totalLength')
for n,d in GraphPath.nodes_iter(data=True):
	if ('ShpName' in d)==True  and totalLength[n]!=0:
		if MinDistance>totalLength[n]: 
			MinDistance=totalLength[n]
			MinDistanceNode=n
#print out results
print "node coordinates "+str(MinDistanceNode)
print "total time for the node "+str(MinDistance)

