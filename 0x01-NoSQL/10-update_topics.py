#!/usr/bin/env python3
''' Change school topics.'''

def update_topics(mongo_collection, name, topics):
    '''changes all the topics of the collection's document based on the name.'''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
