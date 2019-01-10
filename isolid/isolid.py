"""
This module helps to perform some basic Inrupt Solid operations 

"""

import requests
from rdflib import URIRef,Graph,RDF
from rdflib.namespace import FOAF
from loguru import logger


def login(url,username,password):
    "Login into the Solid"
    result_flag = False
    try:
        login  = requests.post(url,username,password)
    except Exception as e:
        logger.debug("\n******\nException when logging into Solid,{}", e)                  
    else:
        result_flag = True

    return result_flag


def get_solid_profile_data(webID):
    "fetch the profile details for the given uri"           
    response=None          
    try:
        headers={'Content-Type': 'text/turtle'}
        response = requests.get(webID,headers)                                                            
        if response.status_code == 200:
            return response.text                                                                                                           
    except Exception as e:        
        logger.debug("\n******\nGET Error: {webid},{}", e, webid=webID)          
        
                                    
def get_rdf_resource_data(uri):
    "Read a RDF resource and returns the data"           
    resource_response=None        
    try:             
        headers={'Content-Type': 'text/turtle'}
        resource_response = requests.ge(uri,headers)                               
        if resource_response.status_code==200:
            return resource_response.text                                 
    except Exception as e:
        logger.debug("\n******\nGET Error: {uri},{}", e, uri=uri)   

    
def get_server_capabilities(uri,capabilities_list):
    "Returns a list of headers describing the server's capabilities."
    option_list=None
    try:
        url = uri+capabilities_list            
        option_list = requests.options(url)                     
        if option_list.status_code==200:                                
            return option_list.text                
    except Exception as e:
        logger.debug("\n******\nGET Error: {url},{}", e, url=url)    

                
def get_friends_list(webID):
    "create, parse graph and get the friends list for the given URI"       
    friends = None 
    try:
        g = create_rdf_graph(webID)   
        for person in g[: RDF.type: FOAF.Person]:
            name = g.value(person, FOAF.name)             
            friends = list(g[person:FOAF.knows])                
            logger.info("{} friends", friends) 
            if friends:                     
                logger.info("{}'s friends:", g.value(person, FOAF.name)) 
    except Exception as e:
        logger.debug("\nException when getting the friends lists,{}", e)                                

    return friends 


def get_subj_pred_object(webID):
    "get subject, predicate and object for the given uri"
    triple_list = []
    try:
        g = create_rdf_graph(webID) 
        for subject,predicate,obj in g:
            triples = subject,predicate,obj
            triple_list.append(triples)            
    except Exception as e:
        logger.debug("\nException when subject, predicate and object,{}", e)              
    
    return triple_list 


def get_subject_list(webID):
    "A generator of subjects with the given predicate and object"
    subject_list = []
    try:
        g = create_rdf_graph(webID)
        subj = g.subjects(predicate=None, object=None)
        for subject in subj:
            subject_list.append(subject)
            subjects = ('\n'.join(subject_list))
    except Exception as e:
        logger.debug("\nException when generating subjects,{}", e)           
    
    return subjects         


def get_predicate_list(webID):
    "get the list of all of the Predicates in the graph"        
    predicate_list = []
    try:
        g = create_rdf_graph(webID)
        preds = g.predicates(subject=None,object=None)
        for predicate in preds:
            predicate_list.append(predicate)
            predicates = ('\n'.join(predicate_list))
    except Exception as e:
        logger.debug("\nException when generating predicates,{}", e)            

    return predicates


def get_object_labels(webID):
    "return a list of objects for the given uri"  
    object_list = [] 
    object_labels = None
    try:
        g = create_rdf_graph(webID) 
        for subject,predicate,obj in g:
            label = obj
            object_list.append(label)
            object_labels = ('\n'.join(object_list))
    except Exception as e:
        logger.debug("\nException when generating list of objects,{}", e)            

    return object_labels           

    
def create_rdf_container(uri,Link,Slug,data):
    "To create a new basic container resource"
    result_flag=False        
    try:                
        response = requests.post(uri,headers={
                                'Content-Type': 'text/turtle',
                                'Link': Link,
                                'Slug': Slug,   
                                'data' : data})            
        if response.status_code==201:
            result_flag=True
    except Exception as e:
        logger.debug("\n******\nPOST Error creating a container resource,{}", e)             
    
    return result_flag         


def create_rdf_resource(uri,Link,Slug,data):
    "To create a new resource"
    result_flag=False
    try:                     
        response = requests.post(uri,headers={
                                'Content-Type': 'text/turtle',
                                'Link': Link,
                                'Slug': Slug,   
                                'data' : data})            
        if response.status_code==201:
            result_flag=True
    except Exception as e:
        logger.debug("\n******\nPOST Error creating a resource,{}", e)              
    
    return result_flag  


def update_rdf_resource(uri,data):
    'updating a RDF resource'
    result_flag=False
    try:                             
        response = requests.put(uri,headers={'Content-Type': 'text/turtle',  
                                'data' : data})                                       
        if response.status_code==201 or response.status_code==204:
            result_flag=True
    except Exception as e:
        logger.debug("\n******\nPUT Error updating a resource,{}", e)               
    
    return result_flag  


def delete_rdf_resource(uri):
    "deleting a RDF resource"
    result_flag=False
    try:                    
        response = requests.delete(uri,headers={'Content-Type': 'text/turtle'})         
        logger.debug("status {}",response.status_code)                                      
        if response.status_code==200 or response.status_code==204:
            result_flag=True                
    except Exception as e:
        logger.debug("\n******\nDELETE Error deleting a resource,{}", e)            
    
    return result_flag         
               
        
def create_rdf_graph(webID):
    "parse a URI into a graph"
    #Create an empty graph that we can load data into
    graph = Graph()
    #Parse the fetched data into the graph
    graph.parse(webID)
    #format of the data into N-triple ('nt')
    graph.serialize(format='nt') 
    
    return graph          


def read_rdf_file(filename):
    "Read a RDF and returns the objects in a rdflib Graph object"
    graph = Graph()
    logger.info("Read RDF data from {}", filename)        
    graph.parse(filename)
    
    return graph    

@logger.catch
def generate_rdfxml_from_rdftriples(webID):
    "generating RDF/XML file from rdf triples"    
    graph = Graph()
    graph.parse(webID)
    rdf_xml = graph.serialize(format='pretty-xml')

    return rdf_xml

