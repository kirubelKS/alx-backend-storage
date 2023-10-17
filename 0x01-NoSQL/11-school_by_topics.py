#!/usr/bin/env python3
'''Where can I learn Python?'''

def school_by_topic(mongo_collection, topic):
    '''Returns the list of students having a specific topics.'''
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
