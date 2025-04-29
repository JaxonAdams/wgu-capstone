from functools import wraps
from datetime import datetime

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
