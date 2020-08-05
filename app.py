#!/usr/bin/env python
# coding: utf-8

# # Brute Force Recommendation


#Import flask and required components
from flask import Flask,request,render_template
import networkx as nx

#Initialize a new app
app = Flask(__name__)


#Home page
@app.route('/')
def index_form():
    return render_template('form.html')

#Home page on submission of form 
@app.route('/',methods=['POST'])
def recommend_tags():
    query_tag = request.form['tag']
    #Read in  graph stored as a pickle
    G = nx.read_gpickle("tags_graph.pickle")
    
    #Query the neighbouring edges of the node 
    edges_of_query = G[query_tag]
    
    #Sort the edges based on edge weights
    neighbours = sorted(edges_of_query.items(), key=lambda edge: edge[1]['weight'],reverse=True)
    
    neighbours_result = '  ||  '.join(neighbour[0] for neighbour in neighbours)
    
    return render_template('recommendation.html',neighbours_result=neighbours_result)
    
     

if __name__ == '__main__':
    app.config['SESSION_COOKIE_SECURE'] = False
    app.run()






