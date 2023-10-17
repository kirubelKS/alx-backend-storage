#!/usr/bin/env python3
''''Where can I learn python?'''

def top_students(mongo_collection):
    '''Print all the students in a collection sorted by average score.'''
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1}
            },
        ]
    )
    return students