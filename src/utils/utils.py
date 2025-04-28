from functools import wraps

def decorate_console_output(msg):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print()
            print("**********")
            print(msg)
            print()
            
            result = func(*args, **kwargs)
            
            print("**********")
            print()
            
            return result
        return wrapper
    return decorator
