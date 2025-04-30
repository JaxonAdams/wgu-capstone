from functools import wraps
from datetime import datetime

import pandas as pd


def decorate_console_output(msg):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print()
            print("**********")
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            print(msg)
            print()
            
            result = func(*args, **kwargs)
            
            print("**********")
            print()
            
            return result
        return wrapper
    return decorator


def read_large_csv(path, chunk_size=100_000):
    
    chunks = []
    for chunk in pd.read_csv(path, low_memory=False, chunksize=chunk_size):
        chunks.append(chunk)
    
    df = pd.concat(chunks, ignore_index=True)
    return df
