def check_if_key_exists(function):
    def wrapper(*args):
        self = args[0]
        key = args[1]
        if key in self.dict:
            value = self.dict[key]
            if not value.is_dead:
                return function(*args)
        return 'KEY DOES NOT EXISTS'
    return wrapper
