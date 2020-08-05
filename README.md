# Stack-Exchange-Tag-Recommendation

Link to the working app : https://stack-ex-tag-app.herokuapp.com/ 

This app allows you to query any of Stack Exchange(Data Science) 's tags and it will return a list of related tags as recommendations . 

A weighted graph of different tags is built using the 'networkx' library . The vertices are the tags and the edge weights indicate the number of times two connected tags appear together in various questions . 

Recommendations are made possible by means of a simple brute force method of querying the graph for related tags. 

The raw data was extracted from the REST API of Stack Exchange. 
