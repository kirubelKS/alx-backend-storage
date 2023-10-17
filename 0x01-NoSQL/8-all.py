#!/usr/bin/env python3
'''List all the documents in python.'''

def list_all(mongo_collection):
    '''lists all the collections in a collection.'''
    return [doc for doc in mongo_collection.find()]
