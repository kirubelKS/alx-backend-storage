#!/usr/bin/env python3
'''Insert a document in python.'''

def insert_school(mongo_collection, **kwargs):
    '''Insert a new document in a colleciton.'''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
