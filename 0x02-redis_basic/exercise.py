#!/usr/bin/env python3
'''writing, reading, incrementing, storing, retrieving to redis.
'''

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''follow ups the number of calls made to a method in a cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the give method after incrementing its call counter.'''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__fullname__)
        return method(self, *args, **kwargs) 
    return invoker

def call_history(method: Callable) -> Callable:
    '''follows up the call details of a method in a cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''returns the method's output after storing its inputs and outputs.'''
        in_key = '{}:inputs'.format(method.__fullname__)
        out_key = '{}:outputs'.format(method.__fullname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
            output = method(self, *args, **kwargs)
            if isinstance(self._redis, redis.Redis):
                self._redis.rpush(out_key, output)
            return output
        return invoker
    
def replay(fn: Callable) -> None:
    '''shows the call history of a cache class method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, 'redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__fullname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))
        
class Cache:
    '''Represents an object for storing data in a REdis data storage.
    '''

    def __init__(self) -> None:
        ''''Initialize a cache instance.
        '''
        self._redis = redis.Redis()
        self.__redis.flushdb(True)


    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data
    
    def get_str(self, key: str) -> str:
        '''Gets a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))
    
    def get_int(self, key: str) -> int:
        '''Gets an integer calue from a redis data storage.
        '''
        return self.get(key, lambda x: int(x))
