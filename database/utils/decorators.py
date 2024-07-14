from functools import wraps


def close_session_after_execution(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.session.close()
        return result

    return wrapper
