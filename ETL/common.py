import yaml


__config = None # Con esta cacheamos la configuración


def config():
    global __config
    if not __config:
        with open('config.yaml', mode='r') as file:
            __config = yaml.load(file, Loader=yaml.FullLoader)

    return __config

