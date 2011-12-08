import exception


def import_class(class_path):
    components = class_path.split('.')
    module_path = '.'.join(components[:-1])
    try:
        mod = __import__(module_path, {}, {}, [])
    except:
        return None
    else:
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod


def handle_response(message):
    if message.action == 'ERROR':
        raise exception.DominusServerError(message.args)
    else:
        raise exception.DominusBadResponse(message)
