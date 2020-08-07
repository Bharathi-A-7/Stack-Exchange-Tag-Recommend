#!/usr/bin/env python
# coding: utf-8

# #Stack Exchange Tag Recommendation 

# # Importing Libraries

import json 
import requests
import networkx as nx
import matplotlib.pyplot as plt
import itertools


# ## Extracting data through API call 

json_list = []

def extract_raw_json():
    
    global json_list
    # make requests for 100 pages of size 100 records each 
    for i in range(1,101):
        url = f'https://api.stackexchange.com/2.2/questions?page={i}&pagesize=100&order=desc&sort=activity&site=datascience&key=4*MX83rbQ8xfUvuY*49ZKw(('
        data = requests.get(url)
        questions_api = data.json()
        json_list.append(questions_api)
    
    #Save the list of extracted records in a json file
    with open('stackExchangeAPI.json', 'w+') as f:
        json.dump(json_list, f, indent=4)
    


# ## Extracting and storing Tags from records

def store_tags():
    #Read each page and record in the file and extract only the tags
    with open('stackExchangeAPI.json','r') as json_file:
        tags_list = []
        data = json.load(json_file)
        for i in range(0,99): #Loop through 100 pages
            for j in range(0,99): # Loop through 100 records in each page
              tags = data[i]["items"][j]["tags"]
              with open('tags.txt','a+') as tags_file: 
                    tags_file.seek(0)
                    d = tags_file.read()
                    #If file contains data , add the record in a newline
                    if len(d) > 0 :
                        tags_file.write("\n")
                    out = ','.join(f'{tags[i]}' for i in range(0,(len(tags))))
                    tags_file.write(out)



#Get list of Unique Tags from tags.txt

unique_tags = []

def extract_unique_tags():
    
    global unique_tags
    fp  = open('tags.txt')
    #Read each line , extract tags split by a comma 
    tags = [word.strip() for line in fp.readlines() for word in line.split(',') if word.strip()]

    print(" Total number of tags : " , len(tags))
    unique_tags = set(tags)   # Find the unique tags
    print(" Number of Unique tags : " , len(unique_tags))


# ## Build a Weighted graph of Tags

#Create an empty graph with no vertices
G = nx.Graph()


def create_nodes():
    global G
    #Create nodes for G 
    for tag in unique_tags:
        G.add_node(tag)
    


def draw_edges():
    global G
    related_tags_in_record = []
    
    fp  = open('tags.txt')
    lines = fp.readlines()

    for line in lines:
            line.strip()
            related_tags_in_record.clear()
            related_tags_in_record.append(line.split(','))
            related_tags_in_record[0] = [e.replace('\n','')for e in related_tags_in_record[0]]
        
            #Checking for edges in all possible pairs of tags in a record
            for i in range(len(related_tags_in_record[0])):
                for j in range(i+1,len(related_tags_in_record[0])):
                    if G.has_edge(related_tags_in_record[0][i],related_tags_in_record[0][j]):
                    # If edge is already present , increase the edge weight by one
                        G[related_tags_in_record[0][i]][related_tags_in_record[0][j]]['weight'] += 1
                    else:
                    # else , draw a new edge
                        G.add_edge(related_tags_in_record[0][i],related_tags_in_record[0][j], weight=1)

    edges_list = G.edges.data('weight', default=1)
    print(edges_list)
    nx.draw(G)

    #Pickling the graph 
    nx.write_gpickle(G,"tags_graph.pickle")
    plt.show()  
    nx.write_gexf(G, "test.gexf")


# # Test Sample Query

#Query the neighbouring nodes(connected) of the query 

def sample_query(query_tag): 
    edges_of_query = G[query_tag]
    
    #Sort the edges based on edge weights
    neighbours = sorted(edges_of_query.items(), key=lambda edge: edge[1]['weight'],reverse=True)

    print(neighbours[:10])
    

#if __name__ == '__main__':
    #extract_raw_json()
    #store_tags()
    

print(json.dumps(json_list[0], indent=4))


extract_unique_tags()


print(list(unique_tags)[:15])


create_nodes()

print(G.nodes)



draw_edges()

sample_query('machine-learning')





